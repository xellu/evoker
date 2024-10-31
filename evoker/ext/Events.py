class EventBus:
    def __init__(self):
        self.events = {
            #event_name: [callbacks]
        }
        
    def attach(self, event_name, callback):
        """
        Register an event callback.
        
        Args:
            event_name (str): The name of the event.
            callback (function): The callback function.
            
        Returns:
            None
        """
        if event_name not in self.events:
            self.events[event_name] = []
            
        self.events[event_name].append(callback)
        
    def detach(self, event_name, callback):
        """
        Remove an event callback.
        
        Args:
            event_name (str): The name of the event.
            callback (function): The callback function.
            
        Returns:
            None
        """
        if event_name not in self.events:
            return
        
        self.events[event_name].remove(callback)
        
    def trigger(self, event_name, *args, **kwargs):
        """
        Trigger an event.
        
        Args:
            event_name (str): The name of the event.
            
        Returns:
            None
        """
        if event_name not in self.events:
            return
        
        for callback in self.events[event_name]:
            callback(*args, **kwargs)
            
    def on(self, event_name):
        """
        Decorator for attaching events.
        
        Args:
            event_name (str): The name of the event.
            
        Returns:
            function: The decorator function.
        """
        def decorator(callback):
            self.attach(event_name, callback)
            return callback
        return decorator