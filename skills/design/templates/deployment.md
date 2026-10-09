---
status: Draft
owner: "<Tech Lead>"
reviewers: ["<SRE>"]
updated_at: "<YYYY-MM-DD>"
feature_size: "<from .size: XS/S/M/L/XL>"
---

# Deployment

<!-- The runtime topology for sad.md §7 (Deployment view): where it runs, how many replicas, where the
     background worker lives, AT WHAT NUMBERS it scales. N/A allowed for XS/S that reuses an existing
     deployment unit with no change. Replace the generic node labels with your real infrastructure. -->

```mermaid
flowchart TB
    subgraph prod[Production]
        subgraph runtime[Runtime environment]
            app1[App instance 1]
            app2[App instance 2]
            appN[App instance N]
        end
        store[(Primary datastore)]
        storeR[(Datastore replica)]
        worker[Background worker]
    end

    LB[Load balancer] --> app1
    LB --> app2
    LB --> appN
    app1 --> store
    app2 --> store
    appN --> store
    app1 -.reads.-> storeR
    worker --> store
```

## Resources / scaling

| Component | Replicas | CPU / mem | Scale trigger |
|---|---|---|---|
| App | <N> | <CPU / mem> | <e.g. CPU > 70%> |
| Background worker | <N> | <CPU / mem> | <manual / queue depth> |
| Datastore | 1 primary + <N> replicas | <CPU / mem> | manual |

## Networking
- <Network policy / transport security / secrets management>
