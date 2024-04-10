import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *


stem_color = "{rgb:red,1;black,0.3}"
conv_color = "{rgb:blue,2;green,1;black,0.3}"
conv_1x1_color = "{rgb:purple,1;black,0.3}"
global_pool_color = "{rgb:yellow,1}"
fc_color = "{rgb:green,1;red,0.5}"

input_size = 512
num_classes = 1
spatial_sizes = [512, 256, 128, 64, 128, 256, 512]
filter_nums = [4, 8, 16, 32, 16, 8, 4]
legend_size = 40

box_size_to_image_ratio = 0.2  # hard set

spatial_scale = 0.05  # scale to spatial_sizes
input_scale = 1.0  # so that input image isnt too big; applies after spatial_scale
filter_scale = 0.3  # scale to filter_nums
layer_filter_scaler = [1.0, 1.0, 0.9, 0.75, 0.9, 1.0, 1.0]  # so that last layers arent too long
output_scale = 1.0  # so that final blocks (spatial or filters) are not too small
#pool_scale = 1.0

legend_y_move = 1
legend_x_move = -1
legend_x_move_second_column = -0.7

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),
    
    #input
    to_input('images/cloud1.png', to="(0,0,0)", 
             height=input_size*spatial_scale*input_scale*box_size_to_image_ratio, width=input_size*spatial_scale*input_scale*box_size_to_image_ratio),
    to_Conv("input_box", offset="(0,0,0)", to="(0,0,0)", caption=f"Input {input_size}x{input_size}", color="{rgb:white,1}", opacity=0.0,
            height=input_size*spatial_scale*input_scale, depth=input_size*spatial_scale*input_scale, width=0.1),

    to_Conv("conv1_1", spatial_size=spatial_sizes[0], filter_num=filter_nums[0], offset="(1.5,0,0)", to="(input_box-east)", color=conv_color,
            height=spatial_sizes[0]*spatial_scale, depth=spatial_sizes[0]*spatial_scale, width=filter_nums[0]*filter_scale*layer_filter_scaler[0]),
    to_dottedEdges("input_box", "conv1_1"),

    to_Conv("conv2_1", spatial_size=spatial_sizes[1], filter_num=filter_nums[1], offset="(1.7,0,0)", to="(conv1_1-east)", color=conv_color,
            height=spatial_sizes[1]*spatial_scale, depth=spatial_sizes[1]*spatial_scale, width=filter_nums[1]*filter_scale*layer_filter_scaler[1]),
    to_connection_down("conv1_1", "conv2_1"),

    to_Conv("conv3_1", spatial_size=spatial_sizes[2], filter_num=filter_nums[2], offset="(1,0,0)", to="(conv2_1-east)", color=conv_color,
            height=spatial_sizes[2]*spatial_scale, depth=spatial_sizes[2]*spatial_scale, width=filter_nums[2]*filter_scale*layer_filter_scaler[2]),
    to_connection_down("conv2_1", "conv3_1"),

    to_Conv("conv4_1", spatial_size=spatial_sizes[3], filter_num=filter_nums[3], offset="(1,0,0)", to="(conv3_1-east)", color=conv_color,
            height=spatial_sizes[3]*spatial_scale, depth=spatial_sizes[3]*spatial_scale, width=filter_nums[3]*filter_scale*layer_filter_scaler[3]),
    to_connection_down("conv3_1", "conv4_1"),

    to_Conv("conv5_1", spatial_size=spatial_sizes[4], filter_num=filter_nums[4], offset="(1,0,0)", to="(conv4_1-east)", color=conv_1x1_color,
            height=spatial_sizes[4]*spatial_scale, depth=spatial_sizes[4]*spatial_scale, width=filter_nums[4]*filter_scale*layer_filter_scaler[4]),
    to_connection_up("conv4_1", "conv5_1"),

    to_Sum("sum1", offset="(0.9,0,0)", to="(conv5_1-east)", radius=30*spatial_scale),
    to_connection("conv5_1", "sum1"),
    to_skip(of='conv3_1', to='sum1', pos=1.5, add_pos=1.12),

    to_Conv("conv6_1", spatial_size=spatial_sizes[4], filter_num=filter_nums[4], offset="(0.7,0,0)", to="(sum1-east)", color=conv_color,
            height=spatial_sizes[4]*spatial_scale, depth=spatial_sizes[4]*spatial_scale, width=filter_nums[4]*filter_scale*layer_filter_scaler[4]),
    to_connection("sum1", "conv6_1"),

    to_Conv("conv7_1", spatial_size=spatial_sizes[5], filter_num=filter_nums[5], offset="(1,0,0)", to="(conv6_1-east)", color=conv_1x1_color,
            height=spatial_sizes[5]*spatial_scale, depth=spatial_sizes[5]*spatial_scale, width=filter_nums[5]*filter_scale*layer_filter_scaler[5]),
    to_connection_up("conv6_1", "conv7_1"),

    to_Sum("sum2", offset="(0.9,0,0)", to="(conv7_1-east)", radius=30*spatial_scale),
    to_connection("conv7_1", "sum2"),
    to_skip(of='conv2_1', to='sum2', pos=1.5, add_pos=3.3),

    to_Conv("conv8_1", spatial_size=spatial_sizes[5], filter_num=filter_nums[5], offset="(0.7,0,0)", to="(sum2-east)", color=conv_color,
            height=spatial_sizes[5]*spatial_scale, depth=spatial_sizes[5]*spatial_scale, width=filter_nums[5]*filter_scale*layer_filter_scaler[5]),
    to_connection("sum2", "conv8_1"),

    to_Conv("conv9_1", spatial_size=spatial_sizes[6], filter_num=filter_nums[6], offset="(2,0,0)", to="(conv8_1-east)", color=conv_1x1_color,
            height=spatial_sizes[6]*spatial_scale, depth=spatial_sizes[6]*spatial_scale, width=filter_nums[6]*filter_scale*layer_filter_scaler[6]),
    to_connection_up("conv8_1", "conv9_1"),

    to_Sum("sum3", offset="(1.4,0,0)", to="(conv9_1-east)", radius=30*spatial_scale),
    to_connection("conv9_1", "sum3"),
    to_skip(of='conv1_1', to='sum3', pos=1.3, add_pos=6),

    to_Conv("conv10_1", filter_num=filter_nums[6], offset="(1.3,0,0)", to="(sum3-east)", color=conv_color,
            height=spatial_sizes[6]*spatial_scale, depth=spatial_sizes[6]*spatial_scale, width=filter_nums[6]*filter_scale*layer_filter_scaler[6]),
    to_connection("sum3", "conv10_1"),

    to_Conv("conv11_1", spatial_size=input_size, offset="(0.2,0,0)", to="(conv10_1-east)", color=conv_1x1_color, caption="Output",
            height=input_size*spatial_scale, depth=input_size*spatial_scale, width=num_classes*filter_scale*output_scale),


    to_output('images/mask1.png', to='(conv11_1-east)', x=2,
              height=input_size*spatial_scale*input_scale*box_size_to_image_ratio, width=input_size*spatial_scale*input_scale*box_size_to_image_ratio),
    to_Conv("output_box", offset="(2,0,0)", to="(conv11_1-east)", caption=f"Mask {input_size}x{input_size}", color="{rgb:white,1}", opacity=0.0,
            height=input_size*spatial_scale*input_scale, depth=input_size*spatial_scale*input_scale, width=0.1),
    to_dottedEdges("conv11_1", "output_box"),

    # Legend
    to_Conv_legend("conv_legend", offset=f"({6.8+legend_x_move},{-4+legend_y_move},0)", to="(0,0,0)", color=conv_color, caption="Conv(k3,s1)+BN+ReLU",
            height=legend_size*spatial_scale, depth=legend_size*spatial_scale, width=legend_size*spatial_scale),
    to_Conv_legend("conv_stem_legend", offset=f"({10+legend_x_move},{-4+legend_y_move},0)", to="(0,0,0)", color=conv_1x1_color, caption="Conv(k1,s1)",
            height=legend_size*spatial_scale, depth=legend_size*spatial_scale, width=legend_size*spatial_scale),
    to_Sum("sum3", offset=f"({13+legend_x_move},{-4+legend_y_move},0)", to="(0,0,0)", radius=30*spatial_scale, caption="Element-wise addition"),
    to_connection_down(f"({6.5+legend_x_move},{-5.5+legend_y_move})", f"({7.5+legend_x_move},{-5.5+legend_y_move})", coords=True, caption="MaxPool"),
    to_connection_up(f"({9.5+legend_x_move},{-5.5+legend_y_move})", f"({10.5+legend_x_move},{-5.5+legend_y_move})", coords=True, caption="Upsample"),
    to_connection(f"({12.5+legend_x_move},{-5.5+legend_y_move})", f"({13.5+legend_x_move},{-5.5+legend_y_move})", coords=True, caption="Identity"),
     
    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()

    '''
    #block-001
    to_ConvConvRelu(name='ccr_b1', s_filer=500, n_filer=(64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40),
    to_dottedEdges("input_box", "ccr_b1"),
    to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.5),
    
    *block_2ConvPool(name='b2', bottom='pool_b1', top='pool_b2', s_filer=256, n_filer=128, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5),
    *block_2ConvPool(name='b3', bottom='pool_b2', top='pool_b3', s_filer=128, n_filer=256, offset="(1,0,0)", size=(25,25,4.5), opacity=0.5),
    *block_2ConvPool(name='b4', bottom='pool_b3', top='pool_b4', s_filer=64,  n_filer=512, offset="(1,0,0)", size=(16,16,5.5), opacity=0.5),

    #Bottleneck
    #block-005
    to_ConvConvRelu(name='ccr_b5', s_filer=32, n_filer=(1024,1024), offset="(2,0,0)", to="(pool_b4-east)", width=(8,8), height=8, depth=8, caption="Bottleneck"),
    to_connection("pool_b4", "ccr_b5"),

    #Decoder
    *block_Unconv(name="b6", bottom="ccr_b5", top='end_b6', s_filer=64,  n_filer=512, offset="(2.1,0,0)", size=(16,16,5.0), opacity=0.5),
    to_skip( of='ccr_b4', to='ccr_res_b6', pos=1.25),
    *block_Unconv(name="b7", bottom="end_b6", top='end_b7', s_filer=128, n_filer=256, offset="(2.1,0,0)", size=(25,25,4.5), opacity=0.5),
    to_skip( of='ccr_b3', to='ccr_res_b7', pos=1.25),    
    *block_Unconv(name="b8", bottom="end_b7", top='end_b8', s_filer=256, n_filer=128, offset="(2.1,0,0)", size=(32,32,3.5), opacity=0.5),
    to_skip( of='ccr_b2', to='ccr_res_b8', pos=1.25),    
    
    *block_Unconv(name="b9", bottom="end_b8", top='end_b9', s_filer=512, n_filer=64,  offset="(2.1,0,0)", size=(40,40,2.5), opacity=0.5),
    to_skip( of='ccr_b1', to='ccr_res_b9', pos=1.25),
    
    to_ConvSoftMax(name="soft1", s_filer=512, offset="(0.75,0,0)", to="(end_b9-east)", width=1, height=40, depth=40, caption="Softmax"),
    to_connection("end_b9", "soft1"),
    '''
