# API (read-only)

GET  /v/{snap}/manifest
GET  /v/{snap}/tile/{tile_id}                 # serves tile_{tile_id}.json.br
POST /v/{snap}/mask                           # returns {mask_id} (future)
GET  /v/{snap}/next?cursor&k&mask_id          # returns stable subsequence (future)
POST /v/{snap}/search                         # {doc_id, order_index} (future)
GET  /v/{snap}/node/{node_id}                 # returns precomputed summary (future)
GET  /v/{snap}/export?mask_id=&fmt=csv|json   # stream ids/stubs (future)
