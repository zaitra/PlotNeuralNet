import os


def to_head(projectpath):
    pathlayers = os.path.join(projectpath, 'layers/').replace('\\', '/')
    return r"""
\documentclass[border=8pt, multi, tikz]{standalone} 
\usepackage{import}
\subimport{"""+ pathlayers + r"""}{init}
\usetikzlibrary{positioning}
\usetikzlibrary{3d} %for including external image 
"""

def to_cor():
    return r"""
\def\ConvColor{rgb:yellow,5;red,2.5;white,5}
\def\ConvReluColor{rgb:yellow,5;red,10;white,5}
\def\PoolColor{rgb:red,1;black,0.3}
\def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
\def\FcColor{rgb:blue,5;red,2.5;white,5}
\def\FcReluColor{rgb:blue,5;red,5;white,4}
\def\SoftmaxColor{rgb:magenta,5;black,7}   
\def\SumColor{rgb:blue,5;green,15}
"""

def to_begin():
    return r"""
\newcommand{\midarrowdown}{\tikz \draw[-Stealth,line width =0.8mm,draw={rgb:red,1;black,0.3}] (-0.3,0) -- ++(0.3,0);}
\newcommand{\midarrowup}{\tikz \draw[-Stealth,line width =0.8mm,draw={rgb:green,1;black,0.3}] (-0.3,0) -- ++(0.3,0);}
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,1;red,1;green,1;black,3}] (-0.3,0) -- ++(0.3,0);}

\begin{document}
\begin{tikzpicture}
\tikzstyle{connection-down}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:red,1;black,0.3},opacity=0.7]
\tikzstyle{connection-up}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:green,1;black,0.3},opacity=0.7]
\tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,1;red,1;green,1;black,3},opacity=0.7]
"""

def to_input(pathfile, to='(-3,0,0)', width=8, height=8, name="input"):
    return r"""
\node[canvas is zy plane at x=0] (""" + name + """) at """+ to +""" {\includegraphics[width="""+ str(width)+"cm"+""",height="""+ str(height)+"cm"+"""]{"""+ pathfile +"""}};
"""

def to_output(pathfile, to='(3,0,0)', width=8, height=8, name="output", x=3):
    return r"""
\node[canvas is zy plane at x="""+ str(x) +"""] (""" + name + """) at """+ to +""" {\includegraphics[width="""+ str(width)+"cm"+""",height="""+ str(height)+"cm"+"""]{"""+ pathfile +"""}};
"""

# Dotted Edges: Connect the dotted edges
def to_dottedEdges(of, to):
    return r"""
\draw [densely dashed]
("""+of+"""-nearnortheast) -- ("""+to+"""-nearnorthwest)
("""+of+"""-nearsoutheast) -- ("""+to+"""-nearsouthwest)
("""+of+"""-farsoutheast) -- ("""+to+"""-farsouthwest)
("""+of+"""-farnortheast) -- ("""+to+"""-farnorthwest);
"""

# Conv
def to_Conv(name, spatial_size=None, filter_num=None, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, opacity=0.7, caption="", color="\ConvReluColor"):
    if spatial_size is None:
        spatial_size = "" 
    if filter_num is None:
        filter_num = ""
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(filter_num) +""", }},
        zlabel="""+ str(spatial_size) +""",
        fill="""+ color +""",
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

def to_Conv_legend(name, spatial_size=None, filter_num=None, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, opacity=0.7, caption="", color="\ConvReluColor"):
    if spatial_size is None:
        spatial_size = "" 
    if filter_num is None:
        filter_num = ""
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption=,
        xlabel={{ """+ '"'+str(caption) +'", "dummy"'+ """ }},
        zlabel="""+ str(spatial_size) +""",
        fill="""+ color +""",
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

def to_ConvRelu(name, spatial_size=None, filter_num=None, offset="(0,0,0)", to="(0,0,0)", width=2, height=40, depth=40, caption="", conv_color="\ConvColor", relu_color="\ConvReluColor"):
    if spatial_size is None:
        spatial_size = "" 
    if filter_num is None:
        filter_num = ""
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption +""",
        xlabel={{ """+ str(filter_num) +""",}},
        zlabel="""+ str(spatial_size) +""",
        fill="""+ conv_color +""",
        bandfill="""+ relu_color +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# Conv,Conv,relu
# Bottleneck
def to_ConvConvRelu(name, s_filer=256, n_filer=(64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption +""",
        xlabel={{ """+ str(n_filer[0]) +""", """+ str(n_filer[1]) +""" }},
        zlabel="""+ str(s_filer) +""",
        fill=\ConvColor,
        bandfill=\ConvReluColor,
        height="""+ str(height) +""",
        width={ """+ str(width[0]) +""" , """+ str(width[1]) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""

# Pool
def to_Pool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=""):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {Box={
        name="""+name+""",
        caption="""+ caption +r""",
        fill=\PoolColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# unpool4, 
def to_UnPool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {Box={
        name="""+ name +r""",
        caption="""+ caption +r""",
        fill=\UnpoolColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

def to_ConvRes(name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=6, height=40, depth=40, opacity=0.2, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name + """,
        caption="""+ caption + """,
        xlabel={{ """+ str(n_filer) + """, }},
        zlabel="""+ str(s_filer) +r""",
        fill={rgb:white,1;black,3},
        bandfill={rgb:white,1;black,2},
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# ConvSoftMax
def to_ConvSoftMax(name, s_filer=40, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" "):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +""",
        zlabel="""+ str(s_filer) +""",
        fill=\SoftmaxColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

def to_FC(name, neurons_num=None, offset="(0,0,0)", to="(0,0,0)", width=1.5, height=3, depth=25, opacity=0.8, caption=" ", color="\SoftmaxColor"):
    if neurons_num is None:
        neurons_num = ""
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +""",
        zlabel="""+ str(neurons_num) +""",
        fill="""+ color +""",
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

def to_Sum(name, offset="(0,0,0)", to="(0,0,0)", radius=2.5, opacity=0.6, caption=""):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Ball={
        name=""" + name +""",
        caption="""+ caption +""",
        fill=\SumColor,
        opacity="""+ str(opacity) +""",
        radius="""+ str(radius) +""",
        logo=$+$
        }
    };
"""

def to_connection_down(of, to, coords=False, caption=""):
    if coords:
        return r"""
\draw [connection-down]  """+ of +"""   -- node {\midarrowdown} node[below=1mm] {"""+ caption +"""} """+ to +""";
"""
    else:
        return r"""
\draw [connection-down] ("""+ of +"""-east)    -- node {\midarrowdown} node[below=1mm] {"""+ caption +"""} ("""+ to +"""-west);
"""

def to_connection_up(of, to, coords=False, caption=""):
    if coords:
        return r"""
\draw [connection-up]  """+ of +"""   -- node {\midarrowup} node[below=1mm] {"""+ caption +"""} """+ to +""";
"""
    else:
        return r"""
\draw [connection-up] ("""+ of +"""-east)    -- node {\midarrowup} node[below=1mm] {"""+ caption +"""} ("""+ to +"""-west);
"""

def to_connection(of, to, coords=False, caption=""):
    if coords:
        return r"""
\draw [copyconnection]  """+ of +"""   -- node {\copymidarrow} node[below=1mm] {"""+ caption +"""} """+ to +""";
"""
    else:
        return r"""
\draw [copyconnection] ("""+ of +"""-east)    -- node {\copymidarrow} node[below=1mm] {"""+ caption +"""} ("""+ to +"""-west);
"""

def to_skip(of, to, pos=1.25, add_pos=0):
    return r"""
\path ("""+ of +"""-southeast) -- ("""+ of +"""-northeast) coordinate[pos="""+ str(pos) +"""] ("""+ of +"""-top) ;
\path ("""+ to +"""-south)  -- ("""+ to +"""-north)  coordinate[pos="""+ str(pos+add_pos) +"""] ("""+ to +"""-top) ;
\draw [copyconnection]  ("""+ of +"""-northeast)  
-- node {\copymidarrow}("""+ of +"""-top)
-- node {\copymidarrow}("""+ to +"""-top)
-- node {\copymidarrow} ("""+ to +"""-north);
"""

def to_end():
    return r"""
\end{tikzpicture}
\end{document}
"""

def to_generate(arch, pathname="file.tex"):
    with open(pathname, "w") as f: 
        for c in arch:
            print(c)
            f.write(c)
