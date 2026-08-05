import { server, expressMiddleware } from './graphql/index.js';
import subscriptions from './subscriptions/index.js';

export default {
  graphql: { server, expressMiddleware },
  subscriptions,
};
