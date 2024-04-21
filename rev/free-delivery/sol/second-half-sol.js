Java.perform(function () {  
	var Activity = Java.use('com.example.freedelivery.MainActivity');

	//Hooks and overrides anti-debugging/emulation functions that cause app to crash
	Activity.V0.implementation = function () {
    		return false;
 	};
  	Activity.P0.implementation = function () {
    		return false;
  	};
	Activity.R0.implementation = function () {
    		return false;
  	};
  	Activity.S0.implementation = function () {
    		return false;
  	};
  	Activity.U0.implementation = function () {
    		return false;
  	};

	//Hooks system call in native code and prints command sent to system
  	Interceptor.attach(Module.findExportByName("libfreedelivery.so", "system"), {
    		onEnter: function(args) {
        		console.log(args[0].readCString());
    		}
	});

	//code for enumerating and hooking native function (not needed for chall but someone might find it useful) 

/*
	var process = Process.enumerateModules()
	var i =0;
	for(i=0;i<process.length;i++){
	if(process[i].path.indexOf('libfreedelivery')!=-1)
	{
	   var exports = process[i].enumerateExports()
	   for(var j =0;j<exports.length;j++){
	   if(exports[j].name.indexOf('Java_')!=-1)
           {	
	      console.log(JSON.stringify(exports[j])+"n")
} } } }
 
  Interceptor.attach(Module.getExportByName('libfreedelivery.so', 'Java_com_example_freedelivery_MainActivity_00024rgae_t'), {
    onEnter: function(args) {
    },
    onLeave: function(retval){
	const dstAddr = Java.vm.getEnv().newStringUtf("Native Hook!");
	retval.replace(dstAddr);
    }
});*/
});
