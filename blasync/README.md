# Blasync
A tiny little library for Blender addons that makes it easy to run code with locking the UI.  
There are 3 important pieces:
 - AsyncModalOperatorMixin  
    Mixin that makes an operator run async non-blocking
 - run_async_blocking(func)  
    function that runs the input function async blocking
 - run_async(func, callback)  
    function that runs the input function async non-blocking and runs the callback once thats done  

Nearly all the code is copied from [ampysprites/blender-asyncio](https://github.com/lampysprites/blender-asyncio) which was copied from Blender Cloud plugin with trivial changes.
