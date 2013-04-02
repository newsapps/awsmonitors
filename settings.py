DEBUG = False

CACHE_FILE = '/tmp/cloudwatch-varnish.csv'
NGINX_CACHE_FILE = '/tmp/cloudwatch-nginx.csv'

# Metrics from varnishstat to report to AWS.
INCLUDE_METRICS = (
    #"client_conn",            # Client connections accepted
    #"client_drop",            # Connection dropped, no sess/wrk
    "client_req",             # Client requests received
    "cache_hit",              # Cache hits
    #"cache_hitpass",          # Cache hits for pass
    "cache_miss",             # Cache misses
    "backend_conn",           # Backend conn. success
    "backend_unhealthy",      # Backend conn. not attempted
    "backend_busy",           # Backend conn. too many
    "backend_fail",           # Backend conn. failures
    #"backend_reuse",          # Backend conn. reuses
    #"backend_toolate",        # Backend conn. was closed
    #"backend_recycle",        # Backend conn. recycles
    #"backend_unused",         # Backend conn. unused
    #"fetch_head",             # Fetch head
    #"fetch_length",           # Fetch with Length
    #"fetch_chunked",          # Fetch chunked
    "fetch_eof",              # Fetch EOF
    "fetch_bad",              # Fetch had bad headers
    "fetch_close",            # Fetch wanted close
    #"fetch_oldhttp",          # Fetch pre HTTP/1.1 closed
    "fetch_zero",             # Fetch zero len
    "fetch_failed",           # Fetch failed
    #"n_sess_mem",             # N struct sess_mem
    #"n_sess",                 # N struct sess
    #"n_object",               # N struct object
    #"n_vampireobject",        # N unresurrected objects
    #"n_objectcore",           # N struct objectcore
    #"n_objecthead",           # N struct objecthead
    #"n_smf",                  # N struct smf
    #"n_smf_frag",             # N small free smf
    #"n_smf_large",            # N large free smf
    #"n_vbe_conn",             # N struct vbe_conn
    #"n_wrk",                  # N worker threads
    #"n_wrk_create",           # N worker threads created
    #"n_wrk_failed",           # N worker threads not created
    #"n_wrk_max",              # N worker threads limited
    #"n_wrk_queue",            # N queued work requests
    #"n_wrk_overflow",         # N overflowed work requests
    #"n_wrk_drop",             # N dropped work requests
    "n_backend",              # N backends
    #"n_expired",              # N expired objects
    #"n_lru_nuked",            # N LRU nuked objects
    #"n_lru_saved",            # N LRU saved objects
    #"n_lru_moved",            # N LRU moved objects
    #"n_deathrow",             # N objects on deathrow
    #"losthdr",                # HTTP header overflows
    #"n_objsendfile",          # Objects sent with sendfile
    #"n_objwrite",             # Objects sent with write
    #"n_objoverflow",          # Objects overflowing workspace
    #"s_sess",                 # Total Sessions
    #"s_req",                  # Total Requests
    #"s_pipe",                 # Total pipe
    #"s_pass",                 # Total pass
    #"s_fetch",                # Total fetch
    #"s_hdrbytes",             # Total header bytes
    #"s_bodybytes",            # Total body bytes
    #"sess_closed",            # Session Closed
    #"sess_pipeline",          # Session Pipeline
    #"sess_readahead",         # Session Read Ahead
    #"sess_linger",            # Session Linger
    #"sess_herd",              # Session herd
    #"shm_records",            # SHM records
    #"shm_writes",             # SHM writes
    #"shm_flushes",            # SHM flushes due to overflow
    #"shm_cont",               # SHM MTX contention
    #"shm_cycles",             # SHM cycles through buffer
    #"sm_nreq",                # allocator requests
    #"sm_nobj",                # outstanding allocations
    #"sm_balloc",              # bytes allocated
    #"sm_bfree",               # bytes free
    #"sma_nreq",               # SMA allocator requests
    #"sma_nobj",               # SMA outstanding allocations
    #"sma_nbytes",             # SMA outstanding bytes
    #"sma_balloc",             # SMA bytes allocated
    #"sma_bfree",              # SMA bytes free
    #"sms_nreq",               # SMS allocator requests
    #"sms_nobj",               # SMS outstanding allocations
    #"sms_nbytes",             # SMS outstanding bytes
    #"sms_balloc",             # SMS bytes allocated
    #"sms_bfree",              # SMS bytes freed
    "backend_req",            # Backend requests made
    #"n_vcl",                  # N vcl total
    #"n_vcl_avail",            # N vcl available
    #"n_vcl_discard",          # N vcl discarded
    #"n_purge",                # N total active purges
    #"n_purge_add",            # N new purges added
    #"n_purge_retire",         # N old purges deleted
    #"n_purge_obj_test",       # N objects tested
    #"n_purge_re_test",        # N regexps tested against
    #"n_purge_dups",           # N duplicate purges removed
    #"hcb_nolock",             # HCB Lookups without lock
    #"hcb_lock",               # HCB Lookups with lock
    #"hcb_insert",             # HCB Inserts
    #"esi_parse",              # Objects ESI parsed (unlock)
    #"esi_errors",             # ESI parse errors (unlock)
    "accept_fail",            # Accept failures
    "client_drop_late",       # Connection dropped late
    #"uptime",                 # Client uptime
    "backend_retry",          # Backend conn. retry
    #"dir_dns_lookups",        # DNS director lookups
    #"dir_dns_failed",         # DNS director failed lookups
    #"dir_dns_hit",            # DNS director cached lookups hit
    #"dir_dns_cache_full",     # DNS director full dnscache
    #"fetch_1xx",              # Fetch no body (1xx)
    #"fetch_204",              # Fetch no body (204)
    #"fetch_304",              # Fetch no body (304)
)

# Many of these metrics are cumulative, so we need to display the delta
# Any keys in this tuple will be reported to AWS as the change since the
# last run, not as the cumulative total.
# TODO: Double check this list
CALCULATE_CHANGE = (
    "client_conn",            # Client connections accepted
    "client_drop",            # Connection dropped, no sess/wrk
    "client_req",             # Client requests received
    "cache_hit",              # Cache hits
    "cache_hitpass",          # Cache hits for pass
    "cache_miss",             # Cache misses
    "backend_conn",           # Backend conn. success
    "backend_unhealthy",      # Backend conn. not attempted
    "backend_busy",           # Backend conn. too many
    "backend_fail",           # Backend conn. failures
    "backend_reuse",          # Backend conn. reuses
    "backend_toolate",        # Backend conn. was closed
    "backend_recycle",        # Backend conn. recycles
    "backend_unused",         # Backend conn. unused
    "fetch_head",             # Fetch head
    "fetch_length",           # Fetch with Length
    "fetch_chunked",          # Fetch chunked
    "fetch_eof",              # Fetch EOF
    "fetch_bad",              # Fetch had bad headers
    "fetch_close",            # Fetch wanted close
    "fetch_oldhttp",          # Fetch pre HTTP/1.1 closed
    "fetch_zero",             # Fetch zero len
    "fetch_failed",           # Fetch failed
    "n_sess_mem",             # N struct sess_mem
    "n_sess",                 # N struct sess
    "n_object",               # N struct object
    "n_vampireobject",        # N unresurrected objects
    "n_objectcore",           # N struct objectcore
    "n_objecthead",           # N struct objecthead
    "n_smf",                  # N struct smf
    "n_smf_frag",             # N small free smf
    "n_smf_large",            # N large free smf
    "n_vbe_conn",             # N struct vbe_conn
    "n_wrk_create",           # N worker threads created
    "n_wrk_failed",           # N worker threads not created
    "n_wrk_max",              # N worker threads limited
    "n_wrk_overflow",         # N overflowed work requests
    "n_wrk_drop",             # N dropped work requests
    "n_expired",              # N expired objects
    "n_lru_nuked",            # N LRU nuked objects
    "n_lru_saved",            # N LRU saved objects
    "n_lru_moved",            # N LRU moved objects
    "n_deathrow",             # N objects on deathrow
    "losthdr",                # HTTP header overflows
    "n_objsendfile",          # Objects sent with sendfile
    "n_objwrite",             # Objects sent with write
    "n_objoverflow",          # Objects overflowing workspace
    "s_sess",                 # Total Sessions
    "s_req",                  # Total Requests
    "s_pipe",                 # Total pipe
    "s_pass",                 # Total pass
    "s_fetch",                # Total fetch
    "s_hdrbytes",             # Total header bytes
    "s_bodybytes",            # Total body bytes
    "sess_closed",            # Session Closed
    "sess_pipeline",          # Session Pipeline
    "sess_readahead",         # Session Read Ahead
    "sess_linger",            # Session Linger
    "sess_herd",              # Session herd
    "shm_records",            # SHM records
    "shm_writes",             # SHM writes
    "shm_flushes",            # SHM flushes due to overflow
    "shm_cont",               # SHM MTX contention
    "shm_cycles",             # SHM cycles through buffer
    "sm_nreq",                # allocator requests
    "sm_nobj",                # outstanding allocations
    "sm_balloc",              # bytes allocated
    "sm_bfree",               # bytes free
    "sma_nreq",               # SMA allocator requests
    "sma_nobj",               # SMA outstanding allocations
    "sma_nbytes",             # SMA outstanding bytes
    "sma_balloc",             # SMA bytes allocated
    "sma_bfree",              # SMA bytes free
    "sms_nreq",               # SMS allocator requests
    "sms_nobj",               # SMS outstanding allocations
    "sms_nbytes",             # SMS outstanding bytes
    "sms_balloc",             # SMS bytes allocated
    "sms_bfree",              # SMS bytes freed
    "backend_req",            # Backend requests made
    "n_vcl",                  # N vcl total
    "n_vcl_avail",            # N vcl available
    "n_vcl_discard",          # N vcl discarded
    "n_purge",                # N total active purges
    "n_purge_add",            # N new purges added
    "n_purge_retire",         # N old purges deleted
    "n_purge_obj_test",       # N objects tested
    "n_purge_re_test",        # N regexps tested against
    "n_purge_dups",           # N duplicate purges removed
    "hcb_nolock",             # HCB Lookups without lock
    "hcb_lock",               # HCB Lookups with lock
    "hcb_insert",             # HCB Inserts
    "esi_parse",              # Objects ESI parsed (unlock)
    "esi_errors",             # ESI parse errors (unlock)
    "accept_fail",            # Accept failures
    "client_drop_late",       # Connection dropped late
    "uptime",                 # Client uptime
    "backend_retry",          # Backend conn. retry
    "dir_dns_lookups",        # DNS director lookups
    "dir_dns_failed",         # DNS director failed lookups
    "dir_dns_hit",            # DNS director cached lookups hit
    "dir_dns_cache_full",     # DNS director full dnscache
    "fetch_1xx",              # Fetch no body (1xx)
    "fetch_204",              # Fetch no body (204)
    "fetch_304",              # Fetch no body (304)
)
