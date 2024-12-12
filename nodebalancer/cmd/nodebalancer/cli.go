package main

import (
	"encoding/json"
	"fmt"
	"strings"
	"sync"
	"time"

	bugout "github.com/bugout-dev/bugout-go/pkg"
	"github.com/bugout-dev/bugout-go/pkg/brood"
	"github.com/google/uuid"
	"github.com/urfave/cli/v2"
)

var CommonCommands = []*cli.Command{
	{
		Name:  "access",
		Usage: "Operations with access IDs as Brood resource",
		Flags: []cli.Flag{},
		Subcommands: []*cli.Command{
			{
				Name:  "add",
				Usage: "Add new user's access ID",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:     "access-token",
						Aliases:  []string{"t"},
						Usage:    "Authorized user access token with granted privileges to create resources in Moonstream Bugout application and sharing read permissions to nodebalancer application user",
						Required: true,
					},
					&cli.StringFlag{
						Name:    "access-id",
						Aliases: []string{"a"},
						Usage:   "UUID for access identification",
					},
					&cli.StringFlag{
						Name:    "user-id",
						Aliases: []string{"u"},
						Usage:   "Bugout user ID",
					},
					&cli.StringFlag{
						Name:     "name",
						Aliases:  []string{"n"},
						Usage:    "Name of the user or application to work with nodebalancer",
						Required: true,
					},
					&cli.StringFlag{
						Name:    "description",
						Aliases: []string{"d"},
					},
					&cli.BoolFlag{
						Name:    "blockchain-access",
						Aliases: []string{"b"},
						Usage:   "Specify this flag to grant direct access to blockchain nodes",
						Value:   true,
					},
					&cli.BoolFlag{
						Name:    "extended-methods",
						Aliases: []string{"e"},
						Usage:   "Specify this flag to grant execution availability to not whitelisted methods",
						Value:   true,
					},
					&cli.UintFlag{
						Name:    "period-duration",
						Aliases: []string{"p"},
						Usage:   "Access period duration in seconds",
						Value:   2592000,
					},
					&cli.UintFlag{
						Name:    "max-calls-per-period",
						Aliases: []string{"m"},
						Usage:   "Max available calls to node during the period",
						Value:   10000,
					},
				},
				Before: func(c *cli.Context) error {
					accessIdFlag := c.String("access-id")
					if accessIdFlag != "" {
						_, uuidErr := uuid.Parse(accessIdFlag)
						if uuidErr != nil {
							return fmt.Errorf("provided --access-id should be valid UUID string")
						}
					}

					periodDurationFlag := c.Uint("period-duration")

					if periodDurationFlag < 3600 {
						return fmt.Errorf("time for --period-duration should be greater then 1 hour")
					}

					return nil
				},
				Action: func(c *cli.Context) error {
					accessToken := c.String("access-token")

					var clientErr error
					bugoutClient, clientErr = CreateBugoutClient()
					if clientErr != nil {
						return clientErr
					}

					newAccess, newErr := AddNewAccess(accessToken, c.String("access-id"), c.String("user-id"), c.String("name"), c.String("description"), c.Bool("blockchain-access"), c.Bool("extended-methods"), c.Uint("period-duration"), c.Uint("max-calls-per-period"))
					if newErr != nil {
						return newErr
					}

					_, shareErr := ShareAccess(accessToken, newAccess.ResourceID, NB_CONTROLLER_USER_ID, "user", DEFAULT_AUTOGENERATED_USER_PERMISSIONS)
					if shareErr != nil {
						return shareErr
					}

					newAccessJson, err := json.Marshal(newAccess)
					if err != nil {
						return fmt.Errorf("unable to encode resource %s data interface to json, err: %v", newAccess.ResourceID, err)
					}
					fmt.Println(string(newAccessJson))

					return nil
				},
			},
			{
				Name:  "update",
				Usage: "Update user's access",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:     "access-token",
						Aliases:  []string{"t"},
						Usage:    "Authorized user access token with granted privileges to updated resources in Moonstream Bugout application",
						Required: true,
					},
					&cli.StringFlag{
						Name:    "access-id",
						Aliases: []string{"a"},
						Usage:   "UUID for access identification",
					},
					&cli.StringFlag{
						Name:    "resource-id",
						Aliases: []string{"r"},
						Usage:   "UUID of Bugout resource for access identification",
					},
					&cli.BoolFlag{
						Name:    "reset-period-start-ts",
						Aliases: []string{"s"},
						Usage:   "Resets access unix period start timestamp to time now",
					},
					&cli.UintFlag{
						Name:    "period-duration",
						Aliases: []string{"p"},
						Usage:   "Access period duration in seconds",
					},
					&cli.UintFlag{
						Name:    "max-calls-per-period",
						Aliases: []string{"m"},
						Usage:   "Max available calls to node during the period",
					},
				},
				Before: func(c *cli.Context) error {
					accessIdFlag := c.String("access-id")
					if accessIdFlag != "" {
						_, uuidErr := uuid.Parse(accessIdFlag)
						if uuidErr != nil {
							return fmt.Errorf("provided --access-id should be valid UUID string")
						}
					}

					if accessIdFlag == "" && c.String("resource-id") == "" {
						return fmt.Errorf("at least one of --access-id or --resource-id should be set")
					}

					if !c.Bool("reset-period-start-ts") && c.Uint("period-duration") == 0 && c.Uint("max-calls-per-period") == 0 {
						return fmt.Errorf("no updated parameters provided, at least one of --reset-period-start-ts or --max-calls-per-period or --period-duration should be set")
					}

					return nil
				},
				Action: func(c *cli.Context) error {
					accessToken := c.String("access-token")

					var clientErr error
					bugoutClient, clientErr = CreateBugoutClient()
					if clientErr != nil {
						return clientErr
					}

					resourceIdFlag := c.String("resource-id")

					var resources *brood.Resources
					var getResErr error
					if resourceIdFlag == "" {
						resources, getResErr = GetResources(accessToken, c.String("access-id"), "")
						if getResErr != nil {
							return getResErr
						}
					} else {
						var resource brood.Resource
						resource, getResErr = bugoutClient.Brood.GetResource(accessToken, resourceIdFlag)
						if getResErr != nil {
							return fmt.Errorf("unable to get Bugout resource, err: %v", getResErr)
						}
						resources = &brood.Resources{Resources: []brood.Resource{resource}}
					}

					if len(resources.Resources) > 1 {
						return fmt.Errorf("too many resources to update")
					} else if len(resources.Resources) == 0 {
						return fmt.Errorf("there are no resources with such parameters")
					}

					clientAccess, parseErr := ParseResourceDataToClientAccess(resources.Resources[0])
					if parseErr != nil {
						return parseErr
					}

					resourceId := clientAccess.ResourceID
					updatedClientAccessResourceData := clientAccess.ClientResourceData
					if c.Bool("reset-period-start-ts") {
						updatedClientAccessResourceData.PeriodStartTs = int64(time.Now().Unix())
					}
					if c.Uint("period-duration") != 0 {
						updatedClientAccessResourceData.PeriodDuration = int64(c.Uint("period-duration"))
					}
					if c.Uint("max-calls-per-period") != 0 {
						updatedClientAccessResourceData.MaxCallsPerPeriod = int64(c.Uint("max-calls-per-period"))
					}

					updatedResource, updErr := bugoutClient.Brood.UpdateResource(accessToken, resourceId, updatedClientAccessResourceData, []string{})
					if updErr != nil {
						return fmt.Errorf("unable to update Bugout resource, err: %v", updErr)
					}

					fmt.Printf("Updated resource %s\n", updatedResource.Id)

					return nil
				},
			},
			{
				Name:  "delete",
				Usage: "Delete user's access",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:     "access-token",
						Aliases:  []string{"t"},
						Usage:    "Authorized user access token with granted privileges to delete resources in Moonstream Bugout application",
						Required: true,
					},
					&cli.StringFlag{
						Name:    "access-id",
						Aliases: []string{"a"},
						Usage:   "UUID for access identification",
					},
					&cli.StringFlag{
						Name:    "user-id",
						Aliases: []string{"u"},
						Usage:   "Filter by user_id",
					},
					&cli.StringFlag{
						Name:    "resource-id",
						Aliases: []string{"r"},
						Usage:   "UUID of Bugout resource for access identification",
					},
				},
				Before: func(c *cli.Context) error {
					accessIdFlag := c.String("access-id")
					if accessIdFlag != "" {
						_, uuidErr := uuid.Parse(accessIdFlag)
						if uuidErr != nil {
							return fmt.Errorf("provided --access-id should be valid UUID string")
						}
					}

					userIdFlag := c.String("user-id")
					resourceIdFlag := c.String("resource-id")

					if accessIdFlag == "" && userIdFlag == "" && resourceIdFlag == "" {
						return fmt.Errorf("at least one of --access-id or --user-id or --resource-id should be set")
					}

					return nil
				},
				Action: func(c *cli.Context) error {
					accessToken := c.String("access-token")

					var clientErr error
					bugoutClient, clientErr = CreateBugoutClient()
					if clientErr != nil {
						return clientErr
					}

					var resources *brood.Resources
					var getResErr error

					resourceIdFlag := c.String("resource-id")
					if resourceIdFlag == "" {
						resources, getResErr = GetResources(accessToken, c.String("access-id"), c.String("user-id"))
						if getResErr != nil {
							return getResErr
						}
					} else {
						var resource brood.Resource
						resource, getResErr = bugoutClient.Brood.GetResource(accessToken, resourceIdFlag)
						if getResErr != nil {
							return fmt.Errorf("unable to get Bugout resource, err: %v", getResErr)
						}
						resources = &brood.Resources{Resources: []brood.Resource{resource}}

					}

					fmt.Printf("Found %d resources to delete\n", len(resources.Resources))
					if len(resources.Resources) == 0 {
						return nil
					}

					var clientAccesses []ClientAccess
					for _, resource := range resources.Resources {
						clientAccess, parseErr := ParseResourceDataToClientAccess(resource)
						if parseErr != nil {
							fmt.Println(parseErr)
							continue
						}

						clientAccesses = append(clientAccesses, *clientAccess)
					}

					for _, access := range clientAccesses {
						fmt.Printf("Deleting resource ID %s with name %s in 3 seconds..\n", access.ResourceID, access.ClientResourceData.Name)
						time.Sleep(3 * time.Second)

						_, delErr := bugoutClient.Brood.DeleteResource(accessToken, access.ResourceID)
						if delErr != nil {
							fmt.Printf("Failed to delete resource with ID %s err: %v\n", access.ResourceID, delErr)
							continue
						}
					}

					return nil
				},
			},
			{
				Name:  "list",
				Usage: "List user accesses",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:     "access-token",
						Aliases:  []string{"t"},
						Usage:    "Authorized user access token with granted privileges to get resources in Moonstream Bugout application",
						Required: true,
					},
					&cli.StringFlag{
						Name:    "access-id",
						Aliases: []string{"a"},
						Usage:   "Filter by access_id",
					},
					&cli.StringFlag{
						Name:    "user-id",
						Aliases: []string{"u"},
						Usage:   "Filter by user_id",
					},
				},
				Action: func(c *cli.Context) error {
					accessToken := c.String("access-token")

					var clientErr error
					bugoutClient, clientErr = CreateBugoutClient()
					if clientErr != nil {
						return clientErr
					}

					resources, getResErr := GetResources(accessToken, c.String("access-id"), c.String("user-id"))
					if getResErr != nil {
						return getResErr
					}

					var clientAccesses []ClientAccess
					for _, resource := range resources.Resources {
						clientAccess, parseErr := ParseResourceDataToClientAccess(resource)
						if parseErr != nil {
							fmt.Println(parseErr)
							continue
						}

						clientAccesses = append(clientAccesses, *clientAccess)
					}

					userAccessesJson, marErr := json.Marshal(clientAccesses)
					if marErr != nil {
						return fmt.Errorf("unable to marshal user accesses struct, err: %v", marErr)
					}
					fmt.Println(string(userAccessesJson))

					return nil
				},
			},
			{
				Name:  "verify",
				Usage: "Verify accesses in correct state",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:     "access-token",
						Aliases:  []string{"t"},
						Usage:    "Authorized user access token with granted privileges to get resources in Moonstream Bugout application",
						Required: true,
					},
				},
				Action: func(c *cli.Context) error {
					accessToken := c.String("access-token")

					var clientErr error
					bugoutClient, clientErr = CreateBugoutClient()
					if clientErr != nil {
						return clientErr
					}

					resources, getResErr := GetResources(accessToken, "", "")
					if getResErr != nil {
						return getResErr
					}

					if len(resources.Resources) == 0 {
						fmt.Println("[]")
						return nil
					}

					var wg sync.WaitGroup
					sem := make(chan struct{}, 3)
					errChan := make(chan error, len(resources.Resources))

					var modifiedClientAccesses []ClientAccess
					var deleteClientAccesses []ClientAccess
					shareResourceIds := make(map[string]bool)
					for _, resource := range resources.Resources {
						wg.Add(1)
						go func(resourceId string) {
							defer wg.Done()
							sem <- struct{}{}

							var isShared bool

							holders, holdErr := bugoutClient.Brood.GetResourceHolders(accessToken, resourceId)
							if holdErr != nil {
								errChan <- fmt.Errorf("failed get holders for resource ID %s with error %v", resourceId, holdErr)
							}

							for _, h := range holders.Holders {
								if h.Id == NB_CONTROLLER_USER_ID {
									isShared = true
								}
							}

							if !isShared {
								shareResourceIds[resourceId] = true
							}

							<-sem
						}(resource.Id)

						var isModified bool
						clientAccess, parseErr := ParseResourceDataToClientAccess(resource)
						if parseErr != nil {
							fmt.Println(parseErr)
							continue
						}

						if clientAccess.ClientResourceData.Name == "" || clientAccess.ClientResourceData.AccessID == "" {
							deleteClientAccesses = append(deleteClientAccesses, *clientAccess)
							continue
						}

						if clientAccess.ClientResourceData.PeriodStartTs == 0 {
							clientAccess.ClientResourceData.PeriodStartTs = int64(time.Now().Unix())
							isModified = true
						}

						if clientAccess.ClientResourceData.PeriodDuration < 3600 {
							clientAccess.ClientResourceData.PeriodDuration = 3600
							isModified = true
						}

						if isModified {
							modifiedClientAccesses = append(modifiedClientAccesses, *clientAccess)
							continue
						}
					}

					fmt.Printf("There are %d accesses to modify:\n", len(modifiedClientAccesses))
					for _, a := range modifiedClientAccesses {
						fmt.Printf("  - resource ID %s with access ID %s\n", a.ResourceID, a.ClientResourceData.AccessID)
					}
					fmt.Printf("There are %d accesses to delete\n", len(deleteClientAccesses))
					for _, a := range deleteClientAccesses {
						fmt.Printf("  - resource ID %s with access ID %s\n", a.ResourceID, a.ClientResourceData.AccessID)
					}

					wg.Wait()
					close(sem)
					close(errChan)

					var errorMessages []string
					for err := range errChan {
						errorMessages = append(errorMessages, err.Error())
					}

					if len(errorMessages) > 0 {
						fmt.Printf("errors occurred during verification:\n%s", strings.Join(errorMessages, "\n"))
					}

					fmt.Printf("There are %d accesses not shared with nodebalancer application user\n", len(shareResourceIds))
					for a := range shareResourceIds {
						fmt.Printf("  - resource ID %s\n", a)
					}

					return nil
				},
			},
		},
	},
	{
		Name:  "server",
		Usage: "Start nodebalancer server",
		Flags: []cli.Flag{
			&cli.StringFlag{
				Name:     "config",
				Aliases:  []string{"c"},
				Usage:    "Path to configuration file",
				Required: true,
			},
			&cli.StringFlag{
				Name:  "host",
				Usage: "Server listening address",
				Value: "127.0.0.1",
			},
			&cli.StringFlag{
				Name:    "port",
				Aliases: []string{"p"},
				Usage:   "Server listening port",
				Value:   "8544",
			},
			&cli.BoolFlag{
				Name:  "healthcheck",
				Usage: "Repeatedly send ping requests to the node to verify its availability",
			},
			&cli.BoolFlag{
				Name:  "debug",
				Usage: "Show extended logs",
			},
		},
		Action: func(c *cli.Context) error {
			NB_ENABLE_DEBUG = c.Bool("debug")

			var clientErr error
			bugoutClient, clientErr = CreateBugoutClient()
			if clientErr != nil {
				return clientErr
			}

			CheckEnvVarSet()

			servErr := Server(c.String("config"), c.String("host"), c.String("port"), c.Bool("healthcheck"))
			if servErr != nil {
				return servErr
			}

			return nil
		},
	},
	{
		Name:  "version",
		Usage: "Shows nodebalancer package version",
		Action: func(cCtx *cli.Context) error {
			fmt.Println(NB_VERSION)
			fmt.Println(bugout.Version)
			return nil
		},
	},
}

func NodebalancerAppCli() *cli.App {
	return &cli.App{
		Name:                 "nodebalancer",
		Version:              fmt.Sprintf("v%s", NB_VERSION),
		Usage:                "Web3 node balancer",
		EnableBashCompletion: true,
		Commands:             CommonCommands,
	}
}
