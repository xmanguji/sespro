
import { createLogger } from 'vuex';
import services from "@/services/API.js";

const mgmLogger = createLogger({
    collapsed: false, // auto-expand logged mutationscollapsed: false, // auto-expand logged mutations
    filter (mutation, stateBefore, stateAfter) {
      // returns `true` if a mutation should be logged
      // `mutation` is a `{ type, payload }`
      console.log(mutation, stateBefore, stateAfter);

      if(mutation.type !== "app/SET_SESSION") {

        const  data = {
          stateBefore: stateBefore,
          stateAfter: stateAfter,
          mutationType: mutation.type,
          mutationPayload: mutation.payload
        }
  
        services.log(stateAfter["app"]["session"], data);
      }

      return mutation.type !== "app/SET_SESSION"
    },
    actionFilter (action, state) {
      // same as `filter` but for actions
      // `action` is a `{ type, payload }`
      console.log("actionFilterState", action, state)
     
      return action.type !== "app/setSession"
    },
    transformer (state) {
      // transform the state before logging it.
      // for example return only a specific sub-tree
      return state
    },
    mutationTransformer (mutation) {
      // mutations are logged in the format of `{ type, payload }`
      // we can format it any way we want.
      return mutation
    },
    actionTransformer (action) {
      // Same as mutationTransformer but for actions
      return action
    },
    logActions: false, // Log Actions
    logMutations: true, // Log mutations
    logger: console, // implementation of the `console` API, default `console`
  })

  export default mgmLogger;