emcc dxgi.cpp -o dxgi.wasm -O3 -s EXPORT_ALL=0 -s EXPORTED_FUNCTIONS="['_sum']"
emcc dxgi.cpp -o dxgi.wasm -O3 -v -s INITIAL_MEMORY=256MB -s MAXIMUM_MEMORY=1GB -s EXPORT_ALL=0 -s EXPORTED_FUNCTIONS="['_process_image', '_alloc_bin', '_alloc_bout']"

// -s ALLOW_MEMORY_GROWTH 

DataViewWidget:vnode_2click_selected: ft:avtx h:c5a0a057 v:b'climate/hp_germany_farmland_fall/zone_0/diffuse_textures_mid_0_0.ddsc'

C Time 0.012518644332885742
C Time 0.012247323989868164
C Time 0.012452840805053711
C Time 0.012439966201782227
C Time 0.012502193450927734

Python Time 0.024748802185058594
Python Time 0.02440786361694336
Python Time 0.024622678756713867
Python Time 0.02463388442993164
Python Time 0.024763107299804688

# PyPy
WASM Time 0.3640730381011963 =  0.15358543395996094 + 0.024332523345947266 + 0.18615508079528809
WASM Time 0.29267144203186035 =  0.1460726261138916 + 0.018781185150146484 + 0.12781763076782227
WASM Time 0.2948896884918213 =  0.14873766899108887 + 0.01877737045288086 + 0.12737464904785156
WASM Time 0.28647565841674805 =  0.14014005661010742 + 0.01883864402770996 + 0.12749695777893066
WASM Time 0.2877676486968994 =  0.1412062644958496 + 0.01900458335876465 + 0.12755680084228516

# LLVM
WASM Time 0.2168431282043457 =  0.19345641136169434 + 0.014397859573364258 + 0.00898885726928711
WASM Time 0.18523454666137695 =  0.1735365390777588 + 0.009010791778564453 + 0.002687215805053711
WASM Time 0.18828964233398438 =  0.1733231544494629 + 0.009198188781738281 + 0.005768299102783203
WASM Time 0.19315028190612793 =  0.1746227741241455 + 0.009212017059326172 + 0.00931549072265625
WASM Time 0.19151973724365234 =  0.17299556732177734 + 0.009221553802490234 + 0.009302616119384766
