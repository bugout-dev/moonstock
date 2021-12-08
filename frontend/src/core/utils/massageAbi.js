const massageAbi = (abi) => {
  const coder = require("web3-eth-abi");
  const getSignature = (item) => {
    console.log("getting key for:", item);
    if (item.type === `function`) {
      const retval = coder.encodeFunctionSignature(item);
      console.log("retval:", retval);
      return retval;
    } else if (item.type === `event`) {
      const retval = coder.encodeEventSignature(item);
      console.log("retval:", retval);
      return retval;
    }
    console.error("item passed to getKay was neither fn neither event!");
  };
  const filtered = abi.filter(
    (item) => item.type === `event` || item.type === `function`
  );

  const signed = filtered.map((item) => {
    item.signature = getSignature(item);
    return item;
  });
  const events = [];
  const functions = [];

  signed.forEach((item) => {
    if (item.type === "event") {
      events.push(item);
    }
    if (item.type === "function") {
      functions.push(item);
    }
  });

  const keyEv = {};
  const keyFn = {};
  console.log("functions:", functions);
  console.log("events:", events);
  const eventsObj =
    events.length > 0
      ? events.reduce(
          (acc, curr) => ((acc[curr.signature] = { ...curr }), keyEv)
        )
      : [];
  const fnsObj =
    functions.length > 0
      ? functions.reduce(
          (acc, curr) => ((acc[curr.signature] = { ...curr }), keyFn)
        )
      : 0;

  return { fnsObj, eventsObj };
};

export default massageAbi;
