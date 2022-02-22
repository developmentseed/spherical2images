from cubemap_splitter import split_cubemap

# Automatically determine format and create new directory with images at original image location
# split_cubemap("data/cubemap.png")

# Specify format and write to user defined directory
split_cubemap("data/cubemap.png", format_type=1, output_directory="data/")
