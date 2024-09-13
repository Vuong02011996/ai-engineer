+ Case 1: Start server: all delete table services_ai => no service ai running
+ Case 2: First came running , len list_all_service_ai = 0
  + Start service 5000, num_cam running = 1
+ Case 3: list_all_service_ai > 0
  + If have service not_run
    + set cam run in service not run
  + If haven't service not_run
    + create new service with num_cam = max_num cam + 1
    + VD: max 5000 => create 5001
  + If haven't service not_run and service running > 5
    + set cam run on default service 5000.