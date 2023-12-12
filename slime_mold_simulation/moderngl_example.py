#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 12:56:41 2023

@author: mer1ch
"""

import moderngl
import numpy as np
from PIL import Image

# Vertex shader code
vertex_shader = """
#version 330

in vec2 in_vert;

void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
}
"""

# Fragment shader code
fragment_shader = """
#version 330

out vec4 fragColor;

void main() {
    fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // Red color
}
"""

# Vertex data for a simple triangle
vertices = np.array([-0.6, -0.6, 0.6, -0.6, 0.0, 0.6], dtype="f4")

# Create a ModernGL context
ctx = moderngl.create_standalone_context()

# Create a shader program
prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

# Create a vertex buffer
vbo = ctx.buffer(vertices)

# Create a vertex array object (VAO)
vao = ctx.simple_vertex_array(prog, vbo, "in_vert")

# Create a framebuffer
fbo = ctx.framebuffer(ctx.renderbuffer((512, 512)))

# Bind the framebuffer
fbo.use()

# Clear the framebuffer
ctx.clear(0.9, 0.9, 0.9)

# Render the triangle
vao.render(moderngl.TRIANGLES)

# Read the framebuffer and save the rendered image
data = fbo.read(components=3)
image = Image.frombytes("RGB", fbo.size, data)
image.save("triangle_render.png")
