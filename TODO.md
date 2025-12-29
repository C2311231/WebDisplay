# To Do Tasks
Transition to a more object orentated system.
    Create Objects for Devices, Screens, Browsers, Criteria, Events (Object that would contain Criterias and Event methods), etc.
    
    Most of these should be models stored into the database:
        Devices would store a refrance to the screens it has
        Events would store a refrance to its events.

    Devices would need to be distinguished local vs remote and be adjusted accordingly.
        Remote device functions should be forwarded to the remote device.
            Remote devices should not manage scheduling or other local only functions but must be able to have that functionality forwarded.
        Local device functions should be handled directly

    Develop the Web Interface into a useable system
    
    Create Universal Serialization and Deserialization methods for objects.
    
    Migrate JS into using objects for Events, Devices, Screens, etc. (Mirror the classes present on the server)
    
    Give js objects methods to refresh data using http/websockets
    Devices
        Screens
        Browsers
        Events
            Criteria
            Actions
            Links to other devices (by id)
        Etc.


    Create a global object managment system, so that a single refrence can be passed to each module and for interdependece they would be able to look up each others objects

    Transition to a more oop friendly design
        Create a Device class and the device would own and be passed to the modules. 
        Seperate out system and device modules.
            System would be made up of single instance long lasting objects that are needed for the most basic operation of the program. (Runs the real program)
                (API, Networking, Web Interface, Updater, etc.)

            Device modules would contain all modules that pertain to a specific device.
                (Version Managment, Events, Screens, Browsers, Scheduling, etc.)
                This allows a single device for example to easily be multiple virtual devices for wireless displays and similar features eventually.
            
    Create API wrappers so that api calls can be easily made through multicast or http.