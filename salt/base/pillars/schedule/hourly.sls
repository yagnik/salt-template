schedule:
  sync_all_hourly:
    function: saltutil.sync_all
    hours: 24
    splay: 2400
