function build() {
    var cmakeJS = require("cmake-js");

    var defaultRuntime = "electron";
    var defaultRuntimeVersion = "11.0.0";

    var options = {
        runtime: process.env.npm_config_wcjs_runtime || undefined,
        runtimeVersion: process.env.npm_config_wcjs_runtime_version || undefined,
        arch: process.env.npm_config_wcjs_arch || undefined
    };

    var buildSystem = new cmakeJS.BuildSystem(options);

    if (buildSystem.options.runtime == undefined) {
        buildSystem.options.runtime = defaultRuntime;
    }

    if (buildSystem.options.runtimeVersion == undefined) {
        buildSystem.options.runtimeVersion = defaultRuntimeVersion;
    }

    buildSystem.rebuild();
}

var times = 0;

function begin() {
    try {
        build();
    }
    catch(e) {
        if (e.code == "MODULE_NOT_FOUND") {
            if (times++ == 5) {
                throw e;
            }
            else {
                setTimeout(begin, 2000);
            }
        }
        else {
            throw e;
        }
    }
};

begin();
