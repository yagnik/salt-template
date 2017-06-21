schedule:
  sync_all_weekly:
    function: saltutil.sync_all
    hours: 24
    splay: 2400
