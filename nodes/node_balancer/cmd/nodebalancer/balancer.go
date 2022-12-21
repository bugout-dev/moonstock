/*
Load balancer logic.
*/
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"sort"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
)

// Main variable of pool of blockchains which contains pool of nodes
// for each blockchain we work during session.

{
	ethereum: {
		{
			external-quicknode: {}
		}
	}
}
var pools map[string]map[string]*NodePool

// Base on CallCounter choosing next node, remove it from mutex and use atomic, it should not be exact correct number

// Use tags as slow way with node pools intersection
tags = [quicknode, external]

map[string][]Node

quicknode = []Node
external = []Node

// do intersection between quicknode and external

for _, node := range nodePool {
	for _, t := range node.Tags {

	}
}

// Node structure with
// StatusURL for status server at node endpoint
// Endpoint for geth/bor/etc node http.server endpoint
type Node struct {
	Endpoint *url.URL

	Tags []string

	Alive        bool
	CurrentBlock uint64
	CallCounter  uint64

	mux sync.RWMutex

	GethReverseProxy *httputil.ReverseProxy
}

type NodePool struct {
	Nodes []*Node

	HighestBlock uint64

	// Counter to observe all nodes
	// Which node we call last one
	Current uint64
}

type BlockchainPool struct {
	Blockchains []*NodePool
}

// Node status response struct for HealthCheck
type NodeStatusResultResponse struct {
	Number string `json:"number"`
}

type NodeStatusResponse struct {
	Result NodeStatusResultResponse `json:"result"`
}

// GenerateIdentifier sorts incoming slice of strings and generate
// output like ["a", "b"] -> "a-b"
func GenerateIdentifier(combination []string) string {
	sort.Strings(combination)

	identifier := ""
	for i, ident := range combination {
		identifier += ident
		if i != len(combination)-1 {
			identifier += "-"
		}
	}

	return identifier
}

// AddNode to the nodes pool
func AddNode(blockchain string, identifier string, node *Node) {
	if pools[blockchain] == nil {
		pools[blockchain] = make(map[string]*NodePool)
	}
	if pools[blockchain][identifier] == nil {
		pools[blockchain][identifier] = &NodePool{}
	}
	pools[blockchain][identifier].Nodes = append(pools[blockchain][identifier].Nodes, node)
}

// SetAlive with mutex for exact node
func (node *Node) SetAlive(alive bool) {
	node.mux.Lock()
	node.Alive = alive
	node.mux.Unlock()
}

// IsAlive returns true when node is alive
func (node *Node) IsAlive() (alive bool) {
	node.mux.RLock()
	alive = node.Alive
	node.mux.RUnlock()
	return alive
}

// UpdateNodeState updates block number and live status,
// also it returns number of time node appeal
func (node *Node) UpdateNodeState(currentBlock uint64, alive bool) (callCounter uint64) {
	node.mux.Lock()
	node.CurrentBlock = currentBlock
	node.Alive = alive

	callCounter = node.CallCounter
	node.mux.Unlock()
	return callCounter
}

// IncreaseCallCounter increased to 1 each time node called
func (node *Node) IncreaseCallCounter() {
	node.mux.Lock()
	if node.CallCounter >= NB_MAX_COUNTER_NUMBER {
		log.Printf("Number of calls for node %s reached %d limit, reset the counter.", node.Endpoint, NB_MAX_COUNTER_NUMBER)
		node.CallCounter = uint64(0)
	} else {
		node.CallCounter++
	}
	node.mux.Unlock()
}

// GetNextNode returns next active peer to take a connection
// Loop through entire nodes to find out an alive one
func GetNextNode(blockchain string, identifier string) *Node {
	np := pools[blockchain][identifier]

	if stateCLI.enableDebugFlag {
		log.Printf("[GetNextNode] Choosing from %d nodes\n", len(np.Nodes))
	}

	// next is an Atomic incrementer, value always in range from 0 to slice length,
	// it returns an index of slice
	nodesLen := len(np.Nodes)
	next := int(atomic.AddUint64(&np.Current, uint64(1)) % uint64(nodesLen))

	// Start from next one and move full cycle
	// If node with not highest block, then go next one, also incrementing Current counter
	for i := next; i < nodesLen+next; i++ {
		// Take an index by modding with length
		idx := i % nodesLen
		// If we have an alive one, use it and store if its not the original one
		if np.Nodes[idx].IsAlive() {
			if i != next {
				atomic.StoreUint64(&np.Current, uint64(idx))
			}

			if (np.Nodes[idx].CurrentBlock + NB_HIGHEST_BLOCK_SHIFT) < np.HighestBlock {
				continue
			}

			if stateCLI.enableDebugFlag {
				fmt.Printf("Chosen node: %v\n", np.Nodes[idx])
			}
			return np.Nodes[idx]
		}
	}
	return nil
}

// SetNodeStatus modify status of the node
func (bpool *BlockchainPool) SetNodeStatus(url *url.URL, alive bool) {
	for _, b := range bpool.Blockchains {
		for _, n := range b.Nodes {
			if n.Endpoint.String() == url.String() {
				n.SetAlive(alive)
				break
			}
		}
	}
}

// StatusLog logs node status
// TODO(kompotkot): Print list of alive and dead nodes
func (bpool *BlockchainPool) StatusLog() {
	for _, b := range bpool.Blockchains {
		for _, n := range b.Nodes {
			log.Printf(
				"[StatusLog] Blockchain %s node %s is alive %t. Blockchain called %d times",
				b.Blockchain, n.Endpoint.Host, n.Alive, b.Current,
			)
		}
	}
}

// HealthCheck fetch the node latest block
func HealthCheck() {
	for blockchain, identifierPools := range pools {
		for identifier, pool := range identifierPools {
			for _, node := range pool.Nodes {
				alive := false

				httpClient := http.Client{Timeout: NB_HEALTH_CHECK_CALL_TIMEOUT}
				resp, err := httpClient.Post(
					node.Endpoint.String(),
					"application/json",
					bytes.NewBuffer([]byte(`{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest", false],"id":1}`)),
				)
				if err != nil {
					node.UpdateNodeState(0, alive)
					log.Printf("Unable to reach node: %s", node.Endpoint.Host)
					continue
				}
				defer resp.Body.Close()

				body, err := ioutil.ReadAll(resp.Body)
				if err != nil {
					node.UpdateNodeState(0, alive)
					log.Printf("Unable to parse response from %s node, err %v", node.Endpoint.Host, err)
					continue
				}

				var statusResponse NodeStatusResponse
				err = json.Unmarshal(body, &statusResponse)
				if err != nil {
					node.UpdateNodeState(0, alive)
					log.Printf("Unable to read json response from %s node, err: %v", node.Endpoint.Host, err)
					continue
				}

				blockNumberHex := strings.Replace(statusResponse.Result.Number, "0x", "", -1)
				blockNumber, err := strconv.ParseUint(blockNumberHex, 16, 64)
				if err != nil {
					node.UpdateNodeState(0, alive)
					log.Printf("Unable to parse block number from hex to string, err: %v", err)
					continue
				}

				// Mark node in list of pool as alive and update current block
				if blockNumber > 0 {
					alive = true
				}
				callCounter := node.UpdateNodeState(blockNumber, alive)
				log.Printf(
					"Node %s is alive: %t with current block: %d called: %d times", node.Endpoint.Host, alive, blockNumber, callCounter,
				)

				if blockNumber > pool.HighestBlock {
					pool.HighestBlock = blockNumber
					log.Printf("Updated HighestBlock to: %d", blockNumber)
				}
			}
		}
	}
}
