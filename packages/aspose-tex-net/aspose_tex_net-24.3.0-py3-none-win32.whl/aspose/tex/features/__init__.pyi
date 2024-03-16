import aspose.tex
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable

class FigureRenderer:
    '''Implements rendering of some LaTeX compact content (supposed to fit one page) and then cropping it from the page.'''
    
    def render(self, latex_body: str, stream: io.BytesIO, figure_renderer_options: aspose.tex.features.FigureRendererOptions) -> aspose.pydrawing.SizeF:
        '''Renders some LaTeX code.
        
        :param latex_body: The LaTeX file body.
        :param stream: The stream to write the output to.
        :param figure_renderer_options: The rendering options.
        :returns: The output image size.'''
        ...
    
    ...

class FigureRendererOptions:
    '''Common options for rendering a LaTeX source code fragment.'''
    
    def __init__(self):
        '''Creates a new instance.'''
        ...
    
    @property
    def preamble(self) -> str:
        '''Gets/sets LaTeX document preamble.'''
        ...
    
    @preamble.setter
    def preamble(self, value: str):
        ...
    
    @property
    def scale(self) -> int:
        '''Gets/set the scale. 1000 means 100%, 1200 means 120%, etc.'''
        ...
    
    @scale.setter
    def scale(self, value: int):
        ...
    
    @property
    def background_color(self) -> aspose.pydrawing.Color:
        '''Gets/sets the background color.'''
        ...
    
    @background_color.setter
    def background_color(self, value: aspose.pydrawing.Color):
        ...
    
    @property
    def log_stream(self) -> io.BytesIO:
        '''Gets/set the stream to write log output to.'''
        ...
    
    @log_stream.setter
    def log_stream(self, value: io.BytesIO):
        ...
    
    @property
    def show_terminal(self) -> bool:
        '''The flag that controls terminal output. If
        true
        
         then terminal output is written to console.'''
        ...
    
    @show_terminal.setter
    def show_terminal(self, value: bool):
        ...
    
    @property
    def error_report(self) -> str:
        '''Gets the error report.'''
        ...
    
    @property
    def required_input_directory(self) -> aspose.tex.io.IInputWorkingDirectory:
        '''Gets/sets the directory for the required input, e.g.,
        packages that are beyond Aspose.TeX's LaTeX support.'''
        ...
    
    @required_input_directory.setter
    def required_input_directory(self, value: aspose.tex.io.IInputWorkingDirectory):
        ...
    
    @property
    def margin(self) -> float:
        '''Gets/sets the margin width.'''
        ...
    
    @margin.setter
    def margin(self, value: float):
        ...
    
    ...

class IRasterRendererOptions:
    '''The interface that defines properties of a raster image renderer.'''
    
    @property
    def resolution(self) -> int:
        '''Gets/sets image resolution.'''
        ...
    
    @resolution.setter
    def resolution(self, value: int):
        ...
    
    ...

class MathRenderer:
    '''Implements rendering of math formula.'''
    
    def render(self, formula: str, stream: io.BytesIO, math_renderer_options: aspose.tex.features.MathRendererOptions) -> aspose.pydrawing.SizeF:
        '''Renders a math formula.
        
        :param formula: The formula LaTeX program.
        :param stream: The stream to write the output to.
        :param math_renderer_options: The rendering options.
        :returns: The output image size.'''
        ...
    
    ...

class MathRendererOptions(aspose.tex.features.FigureRendererOptions):
    '''Math formula common rendering options.'''
    
    def __init__(self):
        '''Creates a new instance.'''
        ...
    
    @property
    def text_color(self) -> aspose.pydrawing.Color:
        '''Gets/sets the formula text color.'''
        ...
    
    @text_color.setter
    def text_color(self, value: aspose.pydrawing.Color):
        ...
    
    ...

class PngFigureRenderer(aspose.tex.features.FigureRenderer):
    '''Implements rendering of some LaTeX compact content (supposed to fit one page) and then cropping it from the page as a PNG image.'''
    
    def __init__(self):
        '''Creates a new instance.'''
        ...
    
    ...

class PngFigureRendererOptions(aspose.tex.features.FigureRendererOptions):
    '''Options for rendering a LaTeX source code fragment to PNG.'''
    
    def __init__(self):
        ...
    
    @property
    def resolution(self) -> int:
        '''Gets/sets image resolution.'''
        ...
    
    @resolution.setter
    def resolution(self, value: int):
        ...
    
    ...

class PngMathRenderer(aspose.tex.features.MathRenderer):
    '''Implements rendering of math formula to PNG.'''
    
    def __init__(self):
        '''Creates a new instance.'''
        ...
    
    ...

class PngMathRendererOptions(aspose.tex.features.MathRendererOptions):
    '''Math formula PNG rendering options.'''
    
    def __init__(self):
        ...
    
    @property
    def resolution(self) -> int:
        '''Gets/sets image resolution.'''
        ...
    
    @resolution.setter
    def resolution(self, value: int):
        ...
    
    ...

class SvgFigureRenderer(aspose.tex.features.FigureRenderer):
    '''Implements rendering of some LaTeX compact content (supposed to fit one page) and then cropping it from the page as an SVG file.'''
    
    def __init__(self):
        '''Creates a new instance.'''
        ...
    
    ...

class SvgFigureRendererOptions(aspose.tex.features.FigureRendererOptions):
    '''Options for rendering a LaTeX source code fragment to SVG.'''
    
    def __init__(self):
        ...
    
    ...

class SvgMathRenderer(aspose.tex.features.MathRenderer):
    '''Implements rendering of math formula to SVG.'''
    
    def __init__(self):
        '''Creates a new instance.'''
        ...
    
    ...

class SvgMathRendererOptions(aspose.tex.features.MathRendererOptions):
    '''Math formula SVG rendering options.'''
    
    def __init__(self):
        ...
    
    ...

