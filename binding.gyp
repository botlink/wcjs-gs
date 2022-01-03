{
  "targets": [{
      "target_name": "wcjs-gs",
      "sources": ["src/JsPlayer.cpp", "src/module.cpp"],
      "include_dirs": [
        "<!@(node -p \"require('node-addon-api').include\")",
        "<!@(node -p \"process.cwd()\")/node_modules/node-addon-api-helpers"
      ],
      "defines": ["NAPI_CPP_EXCEPTIONS", "NAPI_VERSION=6"],
      'conditions': [
          ['OS=="linux"', {
              "cflags!": ["-fno-exceptions"],
              "cflags_cc!": ["-fno-exceptions"],
              "cflags_cc": ["-Wall", "-Wextra", "-pedantic", "-std=c++17"],
              "ldflags": ["-Wl,-rpath,'$$ORIGIN'"],
              "include_dirs": [
                  "<!@(pkg-config --cflags-only-I gstreamer-1.0 | sed s/-I//g)",
                  "<!@(pkg-config --cflags-only-I gstreamer-plugins-base-1.0 | sed s/-I//g)"
              ],
              "libraries": ["<!@(pkg-config --libs gstreamer-1.0)",
                            "<!@(pkg-config --libs gstreamer-plugins-base-1.0)"
              ]
          }],
          ['OS=="mac"', {
              "xcode_settings": {"GCC_ENABLE_CPP_EXCEPTIONS": "YES",
                                 "MACOSX_DEPLOYMENT_TARGET": "10.15",
                                 "OTHER_CFLAGS": ["-Wall", "-Wextra", "-pedantic", "-std=c++17"],
                                 "OTHER_LDFLAGS": ["-Wl,-rpath,@loader_path"]},
              "include_dirs": [
                  "<!@(pkg-config --cflags-only-I gstreamer-1.0 | sed s/-I//g)",
                  "<!@(pkg-config --cflags-only-I gstreamer-plugins-base-1.0 | sed s/-I//g)"
              ],
              "libraries": ["<!@(pkg-config --libs gstreamer-1.0)",
                            "<!@(pkg-config --libs gstreamer-plugins-base-1.0)"
              ]
          }],
          ['OS=="win"', {
	      "defines": [ "_HAS_EXCEPTIONS=1" ],
              "include_dirs": [
	          "$(GSTREAMER_1_0_ROOT_MSVC_X86_64)/include/gstreamer-1.0",
	          "$(GSTREAMER_1_0_ROOT_MSVC_X86_64)/include/glib-2.0",
		  "$(GSTREAMER_1_0_ROOT_MSVC_X86_64)/lib/glib-2.0/include/"
	      ],
	      "msvs_settings": {
	          "VCCLCompilerTool": {
		      "AdditionalOptions": [ "-std:c++17", "/W4" ],
		      "ExceptionHandling": "1"
		  },
		  "VCLinkerTool": {
		    "AdditionalLibraryDirectories": [ "$(GSTREAMER_1_0_ROOT_MSVC_X86_64)/lib" ]
		  }
	      },
	      "libraries": [ "-lgstreamer-1.0.lib", "-lglib-2.0.lib", "-lgobject-2.0.lib",
	                     "-lgstapp-1.0.lib", "-lgstaudio-1.0.lib", "-lgstvideo-1.0.lib",
			     "-lWs2_32.lib" ],
              "copies":[
              ]
          }]
      ],
  },
  {
      "target_name": "action_after_build",
      "type": "none",
      "dependencies": [ "<(module_name)" ],
      "copies": [
        {
          "destination": "<(module_path)",
          "files": [ "<(PRODUCT_DIR)/<(module_name).node" ]
        }
      ]
  }]
}
