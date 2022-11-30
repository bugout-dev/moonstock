import React from "react";
import { VStack, Link, Heading, Icon } from "@chakra-ui/react";
import { getLayout, getLayoutProps } from "../src/layouts/InfoPageLayout";
import { MdPictureAsPdf } from "react-icons/md";

const Papers = () => {
  return (
    <VStack>
      <Heading pb={12} pt="72px">
        Whitepapers
      </Heading>
      <Link
        color="orange.1000"
        href="https://github.com/bugout-dev/moonstream/blob/main/datasets/nfts/papers/ethereum-nfts.pdf"
      >
        An analysis of 7,020,950 NFT transactions on the Ethereum blockchain -
        October 22, 2021
        <Icon as={MdPictureAsPdf} color="red" display="inline-block" />
      </Link>
    </VStack>
  );
};

Papers.getLayout = getLayout;
export async function getStaticProps() {
  const metaTags = {
    title: "Moonstream: Whitepapers",
    description: "Whitepapers by moonstream.to",
    keywords:
      "blockchain, crypto, data, trading, smart contracts, ethereum, solana, transactions, defi, finance, decentralized, analytics, product, whitepapers",
    url: "https://www.moonstream.to/whitepapers",
  };
  const layoutProps = getLayoutProps();
  layoutProps.props.metaTags = { ...layoutProps.props.metaTags, ...metaTags };
  return { ...layoutProps };
}

export default Papers;
