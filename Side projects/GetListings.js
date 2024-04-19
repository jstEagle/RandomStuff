const axios = require('axios');
const apiKey = 'MY_API_KEY(Not included for obvious security reasons.';
const baseURL = 'https://api-mainnet.magiceden.dev/v2';

const api = axios.create({
  baseURL,
  headers: {
    'Authorization': `Bearer ${apiKey}`,
  }
});

const collectionID = 'honeyland_generations_bees';

async function getStats() {
  const endpoint = `/collections/${collectionID}/stats`;
  const queryParams = { listingAggMode: true };

  try {
    const response = await api.get(endpoint, { params: queryParams });
    return response.data;
  } catch (error) {
    console.error('Error getting stats:', error.response ? error.response.data : error.message);
    throw error;
  }
}

async function fetchListingNum() {
  try {
    const { listedCount } = await getStats();
    return listedCount;
  } catch (err) {
    console.error('Error fetching listing count:', err);
    throw err;
  }
}

async function getListings(numItems) {
  const endpoint = `/collections/${collectionID}/listings`;
  const itemsPerPage = 100;
  let page = 1;
  let itemsRemaining = numItems;
  let result = [];

  try {
    while (itemsRemaining > 0) {
      const queryParams = {
        offset: (page - 1) * itemsPerPage,
        limit: Math.min(itemsPerPage, itemsRemaining),
        listingAggMode: true,
      };

      const response = await api.get(endpoint, { params: queryParams });
      const NFTs = response.data;
      itemsRemaining -= NFTs.length;
      console.clear();
      console.log((numItems - itemsRemaining), '/', numItems)
      result.push(...NFTs);
      page++; // Move to the next page

      // Implement rate limiting
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    return result;
  } catch (err) {
    console.error('Error fetching listings:', err);
    throw err;
  }
}


async function main() {
  try {
    const numListings = await fetchListingNum();
    console.log('Total listings:', numListings);

    const NFTs = await getListings(numListings);
    console.log('Fetched listings:', NFTs.length);
    let fp = Infinity;
    NFTs.forEach(item => {
      //For each NFT object, print the market place it is listed on.
      console.log(item.listingSource);
      console.log(item.price);
      console.log();

      if(item.price < fp) fp = item.price;
    });

    console.log('Floor Price: ', fp);
  } catch (err) {
    console.error('Main function error:', err);
  }
}

main();
