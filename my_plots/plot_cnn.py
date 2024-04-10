import sys
sys.path.append('../')
from pycore.tikzeng import *


stem_color = "{rgb:red,1;black,0.3}"
conv_color = "{rgb:blue,2;green,1;black,0.3}"
global_pool_color = "{rgb:yellow,1}"
flatten_color = "{rgb:white,1;black,3}"
fc_color = "{rgb:green,1;red,0.5}"

input_size = 512
num_classes = 1
spatial_sizes = [128, 64, 32, 16, 8]
filter_nums = [4, 8, 16, 32, 64]
legend_size = 12

box_size_to_image_ratio = 0.2  # hard set

spatial_scale = 0.13  # scale to spatial_sizes
input_scale = 0.5  # so that input image isnt too big; applies after spatial_scale
filter_scale = 0.2  # scale to filter_nums
layer_spacial_scaler = [1.0, 1.0, 1.1, 1.3, 1.6]  # so that last layers arent too small
layer_filter_scaler = [1.0, 1.0, 0.9, 0.75, 0.6]  # so that last layers arent too long
output_scale = 1.0  # so that final blocks (spatial or filters) are not too small
#pool_scale = 1.0

legend_y_move = 1
legend_x_move = -3.5
legend_x_move_second_column = -0.7


# defined your arch
arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    to_input('images/cloud1.png', to="(0,0,0)", name='input',
             height=input_size*spatial_scale*input_scale*box_size_to_image_ratio, width=input_size*spatial_scale*input_scale*box_size_to_image_ratio),
    to_Conv("input_box", offset="(0,0,0)", to="(0,0,0)", caption=f"Input {input_size}x{input_size}", color="{rgb:white,1}", opacity=0.0,
            height=input_size*spatial_scale*input_scale, depth=input_size*spatial_scale*input_scale, width=0.1),

    to_Conv("conv_stem", offset="(2,0,0)", to="(input_box-east)", color=stem_color,
            height=spatial_sizes[0]*spatial_scale*layer_spacial_scaler[0], depth=spatial_sizes[0]*spatial_scale*layer_spacial_scaler[0], width=filter_nums[0]*filter_scale*layer_filter_scaler[0]),
    to_dottedEdges("input_box", "conv_stem"),
    to_Conv("conv1_1", filter_num=filter_nums[0], offset="(0,0,0)", to="(conv_stem-east)", color=conv_color,
            height=spatial_sizes[0]*spatial_scale*layer_spacial_scaler[0], depth=spatial_sizes[0]*spatial_scale*layer_spacial_scaler[0], width=filter_nums[0]*filter_scale*layer_filter_scaler[0]),
    to_Conv("conv1_2", spatial_size=spatial_sizes[0], offset="(0,0,0)", to="(conv1_1-east)", color=conv_color,
            height=spatial_sizes[0]*spatial_scale*layer_spacial_scaler[0], depth=spatial_sizes[0]*spatial_scale*layer_spacial_scaler[0], width=filter_nums[0]*filter_scale*layer_filter_scaler[0]),

    # not used because using connection instead of box for pooling makes more sense (pool layer should have same width as conv layers, but that takes up too much space)
    #to_Pool("pool1", offset="(0,0,0)", to="(conv1_2-east)", height=spatial_sizes[1]*spatial_scale, depth=spatial_sizes[1]*spatial_scale, width=1*pool_scale),
    to_Conv("conv2_1", filter_num=filter_nums[1], offset="(1,0,0)", to="(conv1_2-east)", color=conv_color,
            height=spatial_sizes[1]*spatial_scale*layer_spacial_scaler[1], depth=spatial_sizes[1]*spatial_scale*layer_spacial_scaler[1], width=filter_nums[1]*filter_scale*layer_filter_scaler[1]),
    to_connection_down("conv1_2", "conv2_1"),
    to_Conv("conv2_2", spatial_size=spatial_sizes[1], filter_num=filter_nums[1], offset="(0,0,0)", to="(conv2_1-east)", color=conv_color,
            height=spatial_sizes[1]*spatial_scale*layer_spacial_scaler[1], depth=spatial_sizes[1]*spatial_scale*layer_spacial_scaler[1], width=filter_nums[1]*filter_scale*layer_filter_scaler[1]),

    #to_Pool("pool2", offset="(0,0,0)", to="(conv2_2-east)", height=spatial_sizes[2]*spatial_scale, depth=spatial_sizes[2]*spatial_scale, width=1*pool_scale),
    to_Conv("conv3_1", filter_num=filter_nums[2], offset="(1,0,0)", to="(conv2_2-east)", color=conv_color,
            height=spatial_sizes[2]*spatial_scale*layer_spacial_scaler[2], depth=spatial_sizes[2]*spatial_scale*layer_spacial_scaler[2], width=filter_nums[2]*filter_scale*layer_filter_scaler[2]),
    to_connection_down("conv2_2", "conv3_1"),
    to_Conv("conv3_2", spatial_size=spatial_sizes[2], filter_num=filter_nums[2], offset="(0,0,0)", to="(conv3_1-east)", color=conv_color,
             height=spatial_sizes[2]*spatial_scale*layer_spacial_scaler[2], depth=spatial_sizes[2]*spatial_scale*layer_spacial_scaler[2], width=filter_nums[2]*filter_scale*layer_filter_scaler[2]),
    
    #to_Pool("pool3", offset="(0,0,0)", to="(conv3_2-east)", height=spatial_sizes[3]*spatial_scale, depth=spatial_sizes[3]*spatial_scale, width=1*pool_scale),
    to_Conv("conv4_1", filter_num=filter_nums[3], offset="(1,0,0)", to="(conv3_2-east)", color=conv_color,
            height=spatial_sizes[3]*spatial_scale*layer_spacial_scaler[3], depth=spatial_sizes[3]*spatial_scale*layer_spacial_scaler[3], width=filter_nums[3]*filter_scale*layer_filter_scaler[3]),
    to_connection_down("conv3_2", "conv4_1"),
    to_Conv("conv4_2", spatial_size=spatial_sizes[3], filter_num=filter_nums[3], offset="(0,0,0)", to="(conv4_1-east)", color=conv_color,
            height=spatial_sizes[3]*spatial_scale*layer_spacial_scaler[3], depth=spatial_sizes[3]*spatial_scale*layer_spacial_scaler[3], width=filter_nums[3]*filter_scale*layer_filter_scaler[3]),
    
    #to_Pool("pool4", offset="(0,0,0)", to="(conv4_2-east)", height=spatial_sizes[4]*spatial_scale, depth=spatial_sizes[4]*spatial_scale, width=1*pool_scale),
    to_Conv("conv5_1", filter_num=filter_nums[4], offset="(1,0,0)", to="(conv4_2-east)", color=conv_color,
            height=spatial_sizes[4]*spatial_scale*layer_spacial_scaler[4], depth=spatial_sizes[4]*spatial_scale*layer_spacial_scaler[4], width=filter_nums[4]*filter_scale*layer_filter_scaler[4]),
    to_connection_down("conv4_2", "conv5_1"),
    to_Conv("conv5_2", spatial_size=spatial_sizes[4], filter_num=filter_nums[4], offset="(0,0,0)", to="(conv5_1-east)", color=conv_color,
            height=spatial_sizes[4]*spatial_scale*layer_spacial_scaler[4], depth=spatial_sizes[4]*spatial_scale*layer_spacial_scaler[4], width=filter_nums[4]*filter_scale*layer_filter_scaler[4]),

    # global average pooling
    to_Conv("avgpol", spatial_size=1, filter_num=filter_nums[4], offset="(0,0,0)", to="(conv5_2-east)", color=global_pool_color,
            height=1*output_scale, depth=1*output_scale, width=filter_nums[4]*filter_scale*layer_filter_scaler[4]),
    
    # Flatten
    to_FC("flatten", neurons_num=filter_nums[4], offset="(1,0,0)", to="(avgpol-east)", color=flatten_color,
               height=1*output_scale, depth=filter_nums[4]*filter_scale*layer_filter_scaler[4], width=1*output_scale),
    to_dottedEdges("avgpol", "flatten"),

    # Output
    to_FC("soft", neurons_num=num_classes, offset="(1,0,0)", to="(flatten-east)", caption="\nCloudiness", color=fc_color,
               height=1*output_scale, depth=num_classes*output_scale, width=1*output_scale),
    to_dottedEdges("flatten", "soft"),

    # Legend
    to_Conv_legend("conv_stem_legend", offset=f"({16+legend_x_move},{-4+legend_y_move},0)", to="(0,0,0)", color=stem_color, caption="Conv(k4,s4)+BN+ReLU",
            height=legend_size*spatial_scale, depth=legend_size*spatial_scale, width=legend_size*spatial_scale),
    to_Conv_legend("conv_legend", offset=f"({21+legend_x_move+legend_x_move_second_column},{-4+legend_y_move},0)", to="(0,0,0)", color=conv_color, caption="Conv(k3,s1)+BN+ReLU",
            height=legend_size*spatial_scale, depth=legend_size*spatial_scale, width=legend_size*spatial_scale),
    to_Conv_legend("avgpool_legend", offset=f"({16+legend_x_move},{-5.5+legend_y_move},0)", to="(0,0,0)", color=global_pool_color, caption="Global average pooling",
            height=legend_size*spatial_scale, depth=legend_size*spatial_scale, width=legend_size*spatial_scale),
    to_Conv_legend("fc_legend", offset=f"({21+legend_x_move+legend_x_move_second_column},{-5.5+legend_y_move},0)", to="(0,0,0)", color=fc_color, caption="Fully connected", opacity=0.8,
            height=legend_size*spatial_scale, depth=legend_size*spatial_scale, width=legend_size*spatial_scale),
    to_connection_down(f"({15.5+legend_x_move},{-7+legend_y_move})", f"({16.5+legend_x_move},{-7+legend_y_move})", coords=True, caption="MaxPool"),
    to_Conv_legend("flatten_legend", offset=f"({21+legend_x_move+legend_x_move_second_column},{-7+legend_y_move},0)", to="(0,0,0)", color=flatten_color, caption="Flatten", opacity=0.8,
            height=legend_size*spatial_scale, depth=legend_size*spatial_scale, width=legend_size*spatial_scale),

    to_end()
    ]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
