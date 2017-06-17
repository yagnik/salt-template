schedule:
  sync_all_daily:
    function: saltutil.sync_all
    hours: 24
    splay: 2400
