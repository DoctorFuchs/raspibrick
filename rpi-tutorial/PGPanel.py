# PGPanel.py

'''
Class to create a graphics window of default size 501x501 pixels (client drawing area)
using a coordinate system with x-axis from left to right, y-axis from bottom to top
(called window coordinates, default range 0..1, 0..1).
The drawing methods perform drawing operation in an offscreen buffer (pixmap)
and automatically renders it on the screen, so the graphics is shown step-by-step.
User coordinates:  (ux, uy)
Pixel coordinates: (px, py) (screen pixels)
Transformation: px = px(ux), py = py(uy)
Pixel coordinage range: 0..winWidth, 0..winHeight (0,0) upper left corner, x to right, y down
User coordinate range: xmin..xmax, ymin..ymax (0,0) lower left corner, x to right, y up
px = a * ux + b
py = c * uy + d
with a = winWidth / (xmax - xmin)
b = winWidth * xmin / (xmin - xmax)
c = winHeight / (ymin - ymax)
d = winHeight * ymax / (ymax - ymin)
Inverse:
ux = (px - b) / a
uy = (py - d) / c
'''


from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys, time, math
import random

class Size():
    def __init__(self, width, height):
        self.width = width
        self.height = height

class GPanel(QtGui.QWidget):
    def __init__(self, *args):
        '''
        Constructs a GPanel and displays a non-resizable graphics window.
        Defaults with no parameter:
        Window size: 500x500 pixels
        Window title: "GPanel"
        User coordinates: 0, 1, 0, 1
        Background color: white
        Pen color: black
        Pen size: 1

        1 Parameter: Size(window_width, window_height)
        4 Parameters: xmin, xmax, ymin, ymax
        '''
        self._app = QtGui.QApplication(sys.argv)
        super(GPanel, self).__init__()
        self.xmin = 0
        self.xmax = 1
        self.ymin = 0
        self.ymax = 1
        self.winWidth = 500
        self.winHeight = 500
        if not (len(args) == 0 or len(args) == 1 or len(args) == 4):
           raise ValueError("Illegal parameter list")
        if len(args) == 1:
            self.winWidth = args[0].width
            self.winHeight = args[0].height
        elif len(args) == 4:
            self.xmin = args[0]
            self.xmax = args[1]
            self.ymin = args[2]
            self.ymax = args[3]
        self._initUI()

    def _initUI(self):
        self._setDefaults()
        self._label = QLabel()
        self._pixmap = QPixmap(QSize(self.winWidth + 1, self.winHeight + 1))
        self._vbox = QVBoxLayout()
        self._vbox.setContentsMargins(1, 1, 1, 1)
        self.setLayout(self._vbox)
        self._painter = QPainter(self._pixmap)
        self.paintEvent(0)
        self.clear()
        self.show()
        self.setFixedSize(self.winWidth, self.winHeight)

    def _setDefaults(self):
        self.setWindowTitle('GPanel')
        self.penSize = 1
        self.penColor = QColor(0, 0, 0)
        self.bgColor = QColor(255, 255, 255)

        # default pos of GPanel window
        ulx = 10
        uly = 10
        super(GPanel, self).move(ulx, uly)  # position

        self._xCurrent = 0
        self._yCurrent = 0
        self._enableRepaint = True
        self._adjust()
        self._onMousePressed = None
        self._onMouseReleased = None
        self._onMouseMoved = None
        self._isLeftMouseButton = False
        self._isRightMouseButton = False
        self._inMouseMoveCallback = False

    def clear(self):
        '''
        Clears the graphics window and the offscreen buffer used by the window
        (fully paint with background color).
        Sets the current graph cursor position to (0, 0).
        If enableRepaint(false) only clears the offscreen buffer.
        '''
        self._painter.setPen(QPen(self.bgColor, 1))
        self._painter.fillRect(QRect(0, 0, self.winWidth + 1, self.winHeight + 1), self.bgColor)
        self._painter.setPen(QPen(self.penColor, self.penSize))
        self._xCurrent = 0
        self._yCurrent = 0
        if self._enableRepaint:
            self.repaint()

    def erase(self):
        '''
        Same as clear(), but lets the current graph cursor unganged.
        '''
        self._painter.setPen(QPen(self.bgColor, 1))
        self._painter.fillRect(QRect(0, 0, self.winWidth + 1, self.winHeight + 1), self.bgColor)
        self._painter.setPen(QPen(self.penColor, self.penSize))
        if self._enableRepaint:
            self.repaint()

    def keep(self):
        '''
        Blocks until the title bar's close button is hit. Then cleans up
        the graphics system.
        '''
        self._app.exec_()  # blocking
        self._painter.end()
        time.sleep(1)
        sys.exit(0)

    def setTitle(self, title):
        '''
        Sets the title in the window title bar.
        '''
        self.setWindowTitle(title)

    # overwrite
    def paintEvent(self, e):
        self._label.setPixmap(self._pixmap)
        self._vbox.addWidget(self._label)

    def setPenColor(self, *args):
        '''
        Sets the current pen color.
        1 parameter: - string value considered as X11 color string
                     - list considered as [r, b, g] or [r, g, b, a]
                     - tuple considered as (r, b, g) or (r, g, b, a)
        3 parameters: values considered as RGB
        4 parameters: values considered as RGBA
        '''
        if len(args) == 1:
            if type(args[0]) == str:
                try:
                    rgb = x11ColorDict[args[0]]
                except KeyError:
                    raise ValueError("X11 color", args[0], "not found")
                r = rgb[0]
                g = rgb[1]
                b = rgb[2] 
                a = 255
            elif type(args[0]) == list or type(args[0]) == tuple:
                if len(args[0]) == 3:
                    r = args[0][0]
                    g = args[0][1]
                    b = args[0][2]
                    a = 255
                elif len(args[0]) == 4:
                    r = args[0][0]
                    g = args[0][1]
                    b = args[0][2]
                    a = args[0][3]
                else:
                    raise ValueError("Illegal parameter list")
            else:
                raise ValueError("Illegal parameter list")

        elif len(args) == 3:
            r = args[0]
            g = args[1]
            b = args[2] 
            a = 255

        elif len(args) == 4:
            r = args[0]
            g = args[1]
            b = args[2] 
            a = 255

        else:
            raise ValueError("Illegal number of arguments")
            
        self.penColor = QColor(r, g, b, a)
        self._painter.setPen(QPen(self.penColor, self.penSize))
            
    def setPenSize(self, size):
        '''
        Sets the current pen size (width) (>=1).
        Returns the previouis pen size.
        '''
        oldPenSize = self.penSize
        self.penSize = size
        self._painter.setPen(QPen(self.penColor, self.penSize))
        return oldPenSize

    # coordinate transformations
    def toPixel(self, user):
        '''
        Returns pixel coordinates (tuple) of given user coordinates (tupel).
        '''
        return self.toPixelX(user[0]), self.toPixelY(user[1])

    def toPixelX(self, userX):
        '''
        Returns pixel x-coordinate of given user x-coordinate.
        '''
        return (int)(self._a * userX + self._b)

    def toPixelY(self, userY):
        '''
        Returns pixel y-coordinate of given user y-coordinate.
        '''
        return (int)(self._c * userY + self._d)

    def toPixelWidth(self, userWidth):
        '''
        Returns pixel x-increment of given user x-increment (always positive).
        '''
        return int(abs(self._a * userWidth))

    def toPixelHeight(self, userHeight):
        '''
        Returns pixel y-increment of given user y-increment (always positive).
        '''
        return int(abs(self._c * userHeight))

    def toUser(self, pixel):
        '''
        Returns user coordinates (tuple) of given pixel coordinates (tuple).
        '''
        return self.toUserX(pixel[0]), self.toUserY(pixel[1])

    def toUserX(self, pixelX):
        '''
        Returns user x-coordinate of given pixel x-coordinate.
        '''
        a = self.winWidth / (self.xmax - self.xmin)
        b = self.winWidth * self.xmin / (self.xmin - self.xmax)
        return (pixelX - b) / a

    def toUserY(self, pixelY):
        '''
        Returns user y-coordinate of given pixel y-coordinate.
        '''
        c = self.winHeight  / (self.ymin - self.ymax)
        d = self.winHeight * self.ymax / (self.ymax - self.ymin)
        return (pixelY - d) / c

    def toUserWidth(self, pixelWidth):
        '''
        Returns user x-increment of given pixel x-increment (always positive).
        '''
        a = self.winWidth / (self.xmax - self.xmin)
        return abs(pixelWidth / a)

    def toUserHeight(self, pixelHeight):
        '''
        Returns user y-increment of given pixel y-increment (always positive).
        '''
        c = self.winWidth / (self._ymin - self._ymax)
        return abs(pixelHeight / c)

    def setUserCoords(self, xmin, xmax, ymin, ymax):
        '''
        Set user coordinate system left_x, right_x, bottom_y, top_y
        '''
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self._adjust()

    def _adjust(self):
        self._a = self.winWidth / (self.xmax - self.xmin)
        self._b = self.winWidth * self.xmin / (self.xmin - self.xmax)
        self._c = self.winHeight / (self.ymin - self.ymax)
        self._d = self.winHeight * self.ymax / (self.ymax - self.ymin)

    # end of coordinate transformations

    def repaint(self):
        '''
        Renders the offscreen buffer in the graphics window.
        '''
        self.update()
        QApplication.processEvents()

    def enableRepaint(self, enable):
        '''
        Enables/Disables automatic repaint in graphics drawing methods.
        '''
        self._enableRepaint = enable

    def line(self, x1, y1, x2, y2):
        '''
        Draws a line with given user start and end coordinates
        and sets the graph cursor position to the end point.
        '''
        xStart = self.toPixelX(x1)
        yStart = self.toPixelY(y1)
        xEnd = self.toPixelX(x2)
        yEnd = self.toPixelY(y2)
        self._painter.drawLine(xStart, yStart, xEnd, yEnd)
        self._xCurrent = x2
        self._yCurrent = y2
        if self._enableRepaint:
            self.repaint()

    def pos(self, x, y):
        '''
        Sets the current graph cursor position to given user coordinates.
        (without drawing anything, same as move()).
        '''
        self._xCurrent = x
        self._yCurrent = y

    def move(self, x, y):
        # Overrides super.move()
        '''
        Sets the current graph cursor position to given user coordinates.
        (without drawing anything, same as pos()).
        '''
        self.pos(x, y)

    def draw(self, x, y):
        '''
        Draws a line form current graph cursor position to (x, y).
        Sets the graph cursor position to (x, y).
        '''
        self.line(self._xCurrent, self._yCurrent, x, y)

    def getPos():
        '''
        Returns a tuple with current graph cursor position (tuple, user coordinates).
        '''
        return self._xCurrent, self._yCurrent

    def getPosX(self):
        '''
        Returns the current graph cursor x-position (user coordinates).
        '''
        return self._xCurrent

    def getPosY(self):
        '''
        Returns the current graph cursor y-position (user coordinates).
        '''
        return self._yCurrent

    def text(self, *args):
        '''
        Draws a text at given position (user coordinates).
        1 parameter: at current graph cursor position
        3 parameters: x, y, text
        The graph cursor position is unchanged.
        '''
        if len(args) == 1:
            xPos = self.toPixelX(self._xCurrent)
            yPos = self.toPixelY(self._yCurrent)
            text = args[0]
        elif len(args) == 3:
            xPos = self.toPixelX(args[0])
            yPos = self.toPixelY(args[1])
            text = args[2]
        else:
            raise ValueError("Illegal number of arguments")            
            
        self._painter.drawText(xPos, yPos, text)
        if self._enableRepaint:
            self.repaint()

    def addExitListener(self, exitListener):
        '''
        Registers the given function that is called when the title bar
        close button is hit.
        '''
        self._app.aboutToQuit.connect(exitListener)

    def setBgColor(self, *args):
        '''
        Sets the background color. All drawings are erased and the current
        graph cursor is set to (0, 0).
        '''
        if len(args) == 1:
            try:
                rgb = x11ColorDict[args[0]]
            except KeyError:
                raise ValueError("X11 color", args[0], "not found")
            r = rgb[0]
            g = rgb[1]
            b = rgb[2] 
            a = 255
        elif len(args) == 3:
            r = args[0]
            g = args[1]
            b = args[2] 
            a = 255
        elif len(args) == 4:
            r = args[0]
            g = args[1]
            b = args[2] 
            a = 255
        else:
            raise ValueError("Illegal number of arguments")
        self.bgColor = QColor(r, g, b, a)
        self.clear()

        
    def circle(self, r):
        '''
        Draws a circle with center at the current graph cursor position
        with given radius in horizontal window coordinates.
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        rPix = self.toPixelWidth(r)
        self._painter.drawEllipse(QPointF(xPix, yPix), rPix, rPix)
        if self._enableRepaint:
            self.repaint()
        
    def fillCircle(self, r):
        '''
        Draws a filled circle with center at the current graph cursor position
        with given radius in horizontal window coordinates (fill color = pen color).
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        rPix = self.toPixelWidth(r)
        self._painter.setPen(Qt.NoPen)
        self._painter.setBrush(QBrush(self.penColor))
        self._painter.drawEllipse(QPointF(xPix, yPix), rPix, rPix)
        if self._enableRepaint:
            self.repaint()
        self._painter.setPen(QPen(self.penColor, self.penSize))
        self._painter.setBrush(Qt.NoBrush)

 
    def ellipse(self, a, b):
        '''
        Draws an ellipse with center at the current graph cursor position
        with given axes.
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        aPix = self.toPixelWidth(a)
        bPix = self.toPixelHeight(b)
        self._painter.drawEllipse(QPointF(xPix, yPix), aPix, bPix)
        if self._enableRepaint:
            self.repaint()

    def fillEllipse(self, a, b):
        '''
        Draws a filled ellipse with center at the current graph cursor position
        with given axes (fill color = pen color).
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        aPix = self.toPixelWidth(a)
        bPix = self.toPixelHeight(b)
        self._painter.setPen(Qt.NoPen)
        self._painter.setBrush(QBrush(self.penColor))
        self._painter.drawEllipse(QPointF(xPix, yPix), aPix, bPix)
        if self._enableRepaint:
            self.repaint()
        self._painter.setPen(QPen(self.penColor, self.penSize))
        self._painter.setBrush(Qt.NoBrush)

    def rectangle(self, *args):
        '''
        Draws a rectangle. 
        2 parameters: Center at the current graph cursor position
                      and given width and height.
        4 parameters: Given diagonal
        '''
        if len(args) == 2:
            wPix = self.toPixelWidth(args[0])
            hPix = self.toPixelHeight(args[1])
            ulx = self.toPixelX(self._xCurrent) - wPix // 2
            uly = self.toPixelY(self._yCurrent) - hPix // 2
        elif len(args) == 4:
            wPix = self.toPixelWidth(args[2] - args[0])
            hPix = self.toPixelHeight(args[3] - args[1])
            ulx = self.toPixelX(args[0])
            uly = self.toPixelX(args[1])
        self._painter.drawRect(ulx, uly, wPix, hPix)
        if self._enableRepaint:
            self.repaint()

    def fillRectangle(self, *args):
        '''
        Draws a filled rectangle (fill color = pen color).
        2 parameters: Center at the current graph cursor position
                      and given width and height.
        4 parameters: Given diagonal
        '''
        if len(args) == 2:
            wPix = self.toPixelWidth(args[0])
            hPix = self.toPixelHeight(args[1])
            ulx = self.toPixelX(self._xCurrent) - wPix // 2
            uly = self.toPixelX(self._xCurrent) - hPix // 2
        elif len(args) == 4:
            wPix = self.toPixelWidth(args[2] - args[0])
            hPix = self.toPixelHeight(args[3] - args[1])
            ulx = self.toPixelX(args[0])
            uly = self.toPixelX(args[1])
        self._painter.setPen(Qt.NoPen)
        self._painter.setBrush(QBrush(self.penColor))
        self._painter.drawRect(ulx, uly, wPix, hPix)
        if self._enableRepaint:
            self.repaint()
        self._painter.setPen(QPen(self.penColor, self.penSize))
        self._painter.setBrush(Qt.NoBrush)

    def polygon(self, corners):
        '''
        Draws a polygon with given list of vertexes (list of x, y).
        '''
        nodes = []
        for pt in corners:
            node = QPointF(self.toPixelX(pt[0]), self.toPixelY(pt[1]))
            nodes.append(node)
        p = QPolygonF(nodes)
        self._painter.drawPolygon(p)
        if self._enableRepaint:
            self.repaint()

    def fillPolygon(self, corners):
        '''
        Draws a filled polygon with given list of vertexes (list of x, y)
        (fill color = pen color).
        '''
        nodes = []
        for pt in corners:
            node = QPointF(self.toPixelX(pt[0]), self.toPixelY(pt[1]))
            nodes.append(node)
        p = QPolygonF(nodes)
        self._painter.setPen(Qt.NoPen)
        self._painter.setBrush(QBrush(self.penColor))
        self._painter.drawPolygon(p)
        if self._enableRepaint:
            self.repaint()
        self._painter.setPen(QPen(self.penColor, self.penSize))
        self._painter.setBrush(Qt.NoBrush)

    def arc(self, r, startAngle, spanAngle):
        '''
        Draws a circle sector with center at the current graph cursor position,
        given radius and given start and span angles (in degrees, positive
        counter-clockwise, zero to east).
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        rPix = self.toPixelWidth(r)
        topLeft = QPoint(xPix - rPix, yPix - rPix)
        bottomRight = QPoint(xPix + rPix, yPix + rPix)
        rect = QRect(topLeft, bottomRight) 
        self._painter.drawArc(rect, int(16 * startAngle), int(16 * spanAngle))
        if self._enableRepaint:
            self.repaint()

    def fillArc(self, r, startAngle, spanAngle):
        '''
        Draws a filled circle sector with center at the current graph cursor position,
        given radius and given start and span angles (in degrees, positive
        counter-clockwise, zero to east). (fill color = pen color)
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        rPix = self.toPixelWidth(r)
        topLeft = QPoint(xPix - rPix, yPix - rPix)
        bottomRight = QPoint(xPix + rPix, yPix + rPix)
        rect = QRect(topLeft, bottomRight) 
        self._painter.setPen(Qt.NoPen)
        self._painter.setBrush(QBrush(self.penColor))
        self._painter.drawChord(rect, int(16 * startAngle), int(16 * spanAngle))

        # Draw sector triangle
        xStart = int(xPix + rPix * math.cos(math.radians(startAngle)))
        yStart = int(yPix - rPix * math.sin(math.radians(startAngle)))
        xEnd = int(xPix + rPix * math.cos(math.radians(startAngle + spanAngle)))
        yEnd = int(yPix - rPix * math.sin(math.radians(startAngle + spanAngle)))
        triangle = [[xPix, yPix], [xStart, yStart], [xEnd, yEnd]]
        nodes = []        
        for pt in triangle:
            node = QPointF(pt[0], pt[1])
            nodes.append(node)
        p = QPolygonF(nodes)
        self._painter.drawPolygon(p)
     
        if self._enableRepaint:
            self.repaint()
        self._painter.setPen(QPen(self.penColor, self.penSize))
        self._painter.setBrush(Qt.NoBrush)
        
    def chord(self, r, startAngle, spanAngle):
        '''
        Draws a circle chord with center at the current graph cursor position,
        given radius and given start and span angles (in degrees, positive
        counter-clockwise, zero to east).
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        rPix = self.toPixelWidth(r)
        topLeft = QPoint(xPix - rPix, yPix - rPix)
        bottomRight = QPoint(xPix + rPix, yPix + rPix)
        rect = QRect(topLeft, bottomRight) 
        self._painter.drawChord(rect, int(16 * startAngle), int(16 * spanAngle))
        if self._enableRepaint:
            self.repaint()        

    def fillChord(self, r, startAngle, spanAngle):
        '''
        Draws a filled circle chord with center at the current graph cursor position,
        given radius and given start and span angles (in degrees, positive
        counter-clockwise, zero to east). (fill color = pen color)
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        rPix = self.toPixelWidth(r)
        topLeft = QPoint(xPix - rPix, yPix - rPix)
        bottomRight = QPoint(xPix + rPix, yPix + rPix)
        rect = QRect(topLeft, bottomRight) 
        self._painter.setPen(Qt.NoPen)
        self._painter.setBrush(QBrush(self.penColor))
        self._painter.drawChord(rect, int(16 * startAngle), int(16 * spanAngle))
        if self._enableRepaint:
            self.repaint()
        self._painter.setPen(QPen(self.penColor, self.penSize))
        self._painter.setBrush(Qt.NoBrush)

    def startPath(self):
        pass

    def fillPath(self):
        pass
        
    def image(self, imagePath, x, y):
        '''
        Draws the picture with given file path at given upper-left coordinates.
        '''
        img = QImage(imagePath)
        xPix = self.toPixelX(x)
        yPix = self.toPixelY(y)
        self._painter.drawImage(xPix, yPix, img)
        if self._enableRepaint:
            self.repaint()        
       
    def point(self, *args):
        '''
        Draws a single point with current pen size and pen color at given user coordinates.
        No params: draws a current graph cursor position
        '''
        if len(args) == 0:
            xPix = self.toPixelX(self._xCurrent)
            yPix = self.toPixelY(self._yCurrent)
        elif len(args) == 2:
            xPix = self.toPixelX(args[0])
            yPix = self.toPixelY(args[1])
        else:
            raise ValueError("Illegal number of arguments")
        self._painter.drawPoint(QPointF(xPix, yPix))
        if self._enableRepaint:
            self.repaint()
    
    def getPixelColor(self, *args):
        '''
        Returns the RGBA color tuple of a pixel with given user coordinates.
        No params: Returns color at current graph cursor position.
        '''
        if len(args) == 0:
            xPix = self.toPixelX(self._xCurrent)
            yPix = self.toPixelY(self._yCurrent)
        elif len(args) == 2:
            xPix = self.toPixelX(args[0])
            yPix = self.toPixelY(args[1])
        else:
            raise ValueError("Illegal number of parameters.")
        imp = self._pixmap.toImage()
        c = imp.pixel(xPix, yPix)
        return QColor(c).getRgb()  # RGBA    
        
    def fill(self, x, y, color, replacementColor):
        '''
        Fills the closed unicolored region with the inner point (x, y) with
        the given color (RGB, RGBA or X11 color string).
        ''' 
        GPanel.floodFill(self._pixmap, x, y, color, color)

    def getPainter(self):
        '''
        Returns the QPainter reference used to draw into the offscreen buffer.
        ''' 
        return self._painter
        

    def drawGrid(self, *args):
        '''
        Draws a coordinate system with annotated axes. 
        (You must increase the user coordinate system at least 10% in both directions.)
        drawGrid(x, y): Grid with 10 ticks in range 0..x, 0..y. Label text depends if x, y or int or float
        drawGrid(x, y, color): same with given grid color
        drawGrid(x1, x2, y1, y2): same with given span x1..x2, y1..y2
        drawGrid(x1, x2, y1, y2, color): same with given grid color
        drawGrid(x1, x2, y1, y2, x3, y3): same with given number of ticks x3, y3 in x- and y-direction
        '''
        if len(args) == 2:
            self._drawGrid(0, args[0], 0, args[1], 10, 10, None)
        if len(args) == 3:
            self._drawGrid(0, args[0], 0, args[1], 10, 10, args[2])
        elif len(args) == 4:
            self._drawGrid(args[0], args[1], args[2], args[3], 10, 10, None)
        elif len(args) == 5:
            self._drawGrid(args[0], args[1], args[2], args[3], 10, 10, args[4])
        elif len(args) == 6:
            self._drawGrid(args[0], args[1], args[2], args[3], args[4], args[5], None)
        elif len(args) == 7:
            self._drawGrid(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
        else:
            raise ValueError("Illegal number of parameters.")


    def _drawGrid(self, xmin, xmax, ymin, ymax, xticks, yticks, color):
        # Save current cursor and color
        xPos = self.getPosX()
        yPos = self.getPosY()
        if color != None:
           oldColor = self.setColor(color)
        # Horizontal
        for i in range(yticks + 1):
            y = ymin + (ymax - ymin) / float(yticks) * i
            self.line(xmin, y, xmax, y)
            if isinstance(ymin, float) or isinstance(ymax, float):
                self.text(xmin - 0.09 * (xmax - xmin), y, str(y))
            else:
                self.text(xmin - 0.09 * (xmax - xmin), y, str(int(y)))
        # Vertical
        for k in range(xticks + 1):
            x = xmin + (xmax - xmin) / float(xticks) * k
            self.line(x, ymin, x, ymax)
            if isinstance(xmin, float) or isinstance(xmax, float):
                self.text(x, ymin - 0.05 * (ymax - ymin), str(x))
            else:
                self.text(x, ymin - 0.05 * (ymax - ymin), str(int(x)))
        # Restore cursor and color
        self.pos(xPos, yPos)
        if color != None:
           self.setColor(oldColor)

    def addMousePressListener(self, onMousePressed):
        self._onMousePressed = onMousePressed

    def addMouseReleaseListener(self, onMouseReleased):
        self._onMouseReleased = onMouseReleased

    def addMouseMoveListener(self, onMouseMoved):
        self._onMouseMoved = onMouseMoved
        
    def isLeftMouseButton(self):
        return self._isLeftMouseButton

    def isRightMouseButton(self):
        return self._isRightMouseButton
        
    def getScreenWidth(self):
        '''
        Returns the screen width in pixels.
        '''
        screen_resolution = self._app.desktop().screenGeometry()
        return screen_resolution.width()

    def getScreenHeight(self):
        '''
        Returns the screen height in pixels.
        '''
        screen_resolution = self._app.desktop().screenGeometry()
        return screen_resolution.height()
        
        
    def setWindowCenter(self):
        '''
        Sets the screen position to the center of the screen.
        '''
        frameGm = self.frameGeometry()
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        super(GPanel, self).move(frameGm.topLeft())

    def setWindowPos(self, ulx, uly):
        '''
        Sets the screen position of the graphics window.
        '''
        super(GPanel, self).move(ulx, uly)
        
        
    # ------------- Mouse events ----------------------------               
    def mousePressEvent(self, e):
        pos = QPoint(e.pos())
        self._isLeftMouseButton = (e.button() == Qt.LeftButton)
        self._isRightMouseButton = (e.button() != Qt.RightButton)
        if self._onMousePressed != None:
            self._onMousePressed(self.toUserX(pos.x()), self.toUserY(pos.y()))
 
    def mouseReleaseEvent(self, e):
        pos = QPoint(e.pos())
        self._isLeftMouseButton = (e.button() == Qt.LeftButton)
        self._isRightMouseButton = (e.button() != Qt.RightButton)
        if self._onMouseReleased != None:
            self._onMouseReleased(self.toUserX(pos.x()), self.toUserY(pos.y()))

    def mouseMoveEvent(self, e):
        # reject reentrance
        if self._inMouseMoveCallback:
            return
        self._inMouseMoveCallback = True
        pos = QPoint(e.pos())
        if self._onMouseMoved != None:
            self._onMouseMoved(self.toUserX(pos.x()), self.toUserY(pos.y()))
        self._inMouseMoveCallback = False

# ------------- static methods -------------------------------  

    @staticmethod       
    def getDividingPoint(x1, y1, x2, y2, ratio):
        v1 = (x1, y1)
        v2 = (x2, y2)
        dv = (v2[0] - v1[0], v2[1] - v1[1])  # = v2 - v1
        v = (v1[0] + ratio * dv[0], v1[1] + ratio * dv[1]) # v1 + ratio * dv
        return v[0], v[1]   

    @staticmethod       
    def getRandomX11Color():
        return x11colors.getRandomX11Color()

    @staticmethod       
    def floodFill(pm, x, y, oldColor, newColor):
        # Implementation from Hardik Gajjar of algorithm 
        # at http://en.wikipedia.org/wiki/Flood_fill
        '''
        Fills a bounded single-colored region with 
        the given color. The given point is part of the region and used 
        to specify it.
        @param pm the pixmap containing the connected region
        @param pt a point inside the region
        @param oldColor the old color of the region
        @param newColor the new color of the region
        @return a new pixmap with the transformed region, the given pixmap
        remains unchanged
        '''
        image = QPixmap(pm.width(), pm.height())
        '''
    Graphics2D g2D = image.createGraphics();
    g2D.drawImage(bi, 0, 0, null);

    int oldRGB = oldColor.getRGB();
    int newRGB = newColor.getRGB();

    // Perform filling operation
    Queue<Point> q = new LinkedList<Point>();
    q.add(pt);
    while (q.size() > 0)
    {
      Point n = q.poll();
      if (image.getRGB(n.x, n.y) != oldRGB)
        continue;

      Point w = n, e = new Point(n.x + 1, n.y);
      while ((w.x > 0) && (image.getRGB(w.x, w.y) == oldRGB))
      {
        image.setRGB(w.x, w.y, newRGB);
        if ((w.y > 0) && (image.getRGB(w.x, w.y - 1) == oldRGB))
          q.add(new Point(w.x, w.y - 1));
        if ((w.y < image.getHeight() - 1)
          && (image.getRGB(w.x, w.y + 1) == oldRGB))
          q.add(new Point(w.x, w.y + 1));
        w.x--;
      }
      while ((e.x < image.getWidth() - 1)
        && (image.getRGB(e.x, e.y) == oldRGB))
      {
        image.setRGB(e.x, e.y, newRGB);

        if ((e.y > 0) && (image.getRGB(e.x, e.y - 1) == oldRGB))
          q.add(new Point(e.x, e.y - 1));
        if ((e.y < image.getHeight() - 1)
          && (image.getRGB(e.x, e.y + 1) == oldRGB))
          q.add(new Point(e.x, e.y + 1));
        e.x++;
      }
    }
    '''
        return image;

    @staticmethod       
    def getRandomX11Color():
        r = random.randint(0, 540)
        c = list(x11ColorDict.keys())
        return c[r]
           

x11ColorDict = {
"aqua":[0, 255, 255],
"cornflower":[100, 149, 237],
"crimson":[220, 20, 60],
"fuchsia":[255, 0, 255],
"indigo":[75, 0, 130],
"lime":[50, 205, 50],
"silver":[192, 192, 192],
"ghost white":[248, 248, 255],
"snow":[255, 250, 250],
"ghostwhite":[248, 248, 255],
"white smoke":[245, 245, 245],
"whitesmoke":[245, 245, 245],
"gainsboro":[220, 220, 220],
"floral white":[255, 250, 240],
"floralwhite":[255, 250, 240],
"old lace":[253, 245, 230],
"oldlace":[253, 245, 230],
"linen":[250, 240, 230],
"antique white":[250, 235, 215],
"antiquewhite":[250, 235, 215],
"papaya whip":[255, 239, 213],
"papayawhip":[255, 239, 213],
"blanched almond":[255, 235, 205],
"blanchedalmond":[255, 235, 205],
"bisque":[255, 228, 196],
"peach puff":[255, 218, 185],
"peachpuff":[255, 218, 185],
"navajo white":[255, 222, 173],
"navajowhite":[255, 222, 173],
"moccasin":[255, 228, 181],
"cornsilk":[255, 248, 220],
"ivory":[255, 255, 240],
"lemon chiffon":[255, 250, 205],
"lemonchiffon":[255, 250, 205],
"seashell":[255, 245, 238],
"honeydew":[240, 255, 240],
"mint cream":[245, 255, 250],
"mintcream":[245, 255, 250],
"azure":[240, 255, 255],
"alice blue":[240, 248, 255],
"aliceblue":[240, 248, 255],
"lavender":[230, 230, 250],
"lavender blush":[255, 240, 245],
"lavenderblush":[255, 240, 245],
"misty rose":[255, 228, 225],
"mistyrose":[255, 228, 225],
"white":[255, 255, 255],
"black":[0, 0, 0],
"dark slate gray":[47, 79, 79],
"darkslategray":[47, 79, 79],
"dark slate grey":[47, 79, 79],
"darkslategrey":[47, 79, 79],
"dim gray":[105, 105, 105],
"dimgray":[105, 105, 105],
"dim grey":[105, 105, 105],
"dimgrey":[105, 105, 105],
"slate gray":[112, 128, 144],
"slategray":[112, 128, 144],
"slate grey":[112, 128, 144],
"slategrey":[112, 128, 144],
"light slate gray":[119, 136, 153],
"lightslategray":[119, 136, 153],
"light slate grey":[119, 136, 153],
"lightslategrey":[119, 136, 153],
"gray":[190, 190, 190],
"grey":[190, 190, 190],
"light grey":[211, 211, 211],
"lightgrey":[211, 211, 211],
"light gray":[211, 211, 211],
"lightgray":[211, 211, 211],
"midnight blue":[25, 25, 112],
"midnightblue":[25, 25, 112],
"navy":[0, 0, 128],
"navy blue":[0, 0, 128],
"navyblue":[0, 0, 128],
"cornflower blue":[100, 149, 237],
"cornflowerblue":[100, 149, 237],
"dark slate blue":[72, 61, 139],
"darkslateblue":[72, 61, 139],
"slate blue":[106, 90, 205],
"slateblue":[106, 90, 205],
"medium slate blue":[123, 104, 238],
"mediumslateblue":[123, 104, 238],
"light slate blue":[132, 112, 255],
"lightslateblue":[132, 112, 255],
"medium blue":[0, 0, 205],
"mediumblue":[0, 0, 205],
"royal blue":[65, 105, 225],
"royalblue":[65, 105, 225],
"blue":[0, 0, 255],
"dodger blue":[30, 144, 255],
"dodgerblue":[30, 144, 255],
"deep sky blue":[0, 191, 255],
"deepskyblue":[0, 191, 255],
"sky blue":[135, 206, 235],
"skyblue":[135, 206, 235],
"light sky blue":[135, 206, 250],
"lightskyblue":[135, 206, 250],
"steel blue":[70, 130, 180],
"steelblue":[70, 130, 180],
"light steel blue":[176, 196, 222],
"lightsteelblue":[176, 196, 222],
"light blue":[173, 216, 230],
"lightblue":[173, 216, 230],
"powder blue":[176, 224, 230],
"powderblue":[176, 224, 230],
"pale turquoise":[175, 238, 238],
"paleturquoise":[175, 238, 238],
"dark turquoise":[0, 206, 209],
"darkturquoise":[0, 206, 209],
"medium turquoise":[72, 209, 204],
"mediumturquoise":[72, 209, 204],
"turquoise":[64, 224, 208],
"cyan":[0, 255, 255],
"light cyan":[224, 255, 255],
"lightcyan":[224, 255, 255],
"cadet blue":[95, 158, 160],
"cadetblue":[95, 158, 160],
"medium aquamarine":[102, 205, 170],
"mediumaquamarine":[102, 205, 170],
"aquamarine":[127, 255, 212],
"dark green":[0, 100, 0],
"darkgreen":[0, 100, 0],
"dark olive green":[85, 107, 47],
"darkolivegreen":[85, 107, 47],
"dark sea green":[143, 188, 143],
"darkseagreen":[143, 188, 143],
"sea green":[46, 139, 87],
"seagreen":[46, 139, 87],
"medium sea green":[60, 179, 113],
"mediumseagreen":[60, 179, 113],
"light sea green":[32, 178, 170],
"lightseagreen":[32, 178, 170],
"pale green":[152, 251, 152],
"palegreen":[152, 251, 152],
"spring green":[0, 255, 127],
"springgreen":[0, 255, 127],
"lawn green":[124, 252, 0],
"lawngreen":[124, 252, 0],
"green":[0, 255, 0],
"chartreuse":[127, 255, 0],
"medium spring green":[0, 250, 154],
"mediumspringgreen":[0, 250, 154],
"green yellow":[173, 255, 47],
"greenyellow":[173, 255, 47],
"lime green":[50, 205, 50],
"limegreen":[50, 205, 50],
"yellow green":[154, 205, 50],
"yellowgreen":[154, 205, 50],
"forest green":[34, 139, 34],
"forestgreen":[34, 139, 34],
"olive drab":[107, 142, 35],
"olivedrab":[107, 142, 35],
"dark khaki":[189, 183, 107],
"darkkhaki":[189, 183, 107],
"khaki":[240, 230, 140],
"pale goldenrod":[238, 232, 170],
"palegoldenrod":[238, 232, 170],
"light goldenrod yellow":[250, 250, 210],
"lightgoldenrodyellow":[250, 250, 210],
"light yellow":[255, 255, 224],
"lightyellow":[255, 255, 224],
"yellow":[255, 255, 0],
"gold":[255, 215, 0],
"light goldenrod":[238, 221, 130],
"lightgoldenrod":[238, 221, 130],
"goldenrod":[218, 165, 32],
"dark goldenrod":[184, 134, 11],
"darkgoldenrod":[184, 134, 11],
"rosy brown":[188, 143, 143],
"rosybrown":[188, 143, 143],
"indian red":[205, 92, 92],
"indianred":[205, 92, 92],
"saddle brown":[139, 69, 19],
"saddlebrown":[139, 69, 19],
"sienna":[160, 82, 45],
"peru":[205, 133, 63],
"burlywood":[222, 184, 135],
"beige":[245, 245, 220],
"wheat":[245, 222, 179],
"sandy brown":[244, 164, 96],
"sandybrown":[244, 164, 96],
"tan":[210, 180, 140],
"chocolate":[210, 105, 30],
"firebrick":[178, 34, 34],
"brown":[165, 42, 42],
"dark salmon":[233, 150, 122],
"darksalmon":[233, 150, 122],
"salmon":[250, 128, 114],
"light salmon":[255, 160, 122],
"lightsalmon":[255, 160, 122],
"orange":[255, 165, 0],
"dark orange":[255, 140, 0],
"darkorange":[255, 140, 0],
"coral":[255, 127, 80],
"light coral":[240, 128, 128],
"lightcoral":[240, 128, 128],
"tomato":[255, 99, 71],
"orange red":[255, 69, 0],
"orangered":[255, 69, 0],
"red":[255, 0, 0],
"hot pink":[255, 105, 180],
"hotpink":[255, 105, 180],
"deep pink":[255, 20, 147],
"deeppink":[255, 20, 147],
"pink":[255, 192, 203],
"light pink":[255, 182, 193],
"lightpink":[255, 182, 193],
"pale violet red":[219, 112, 147],
"palevioletred":[219, 112, 147],
"maroon":[176, 48, 96],
"medium violet red":[199, 21, 133],
"mediumvioletred":[199, 21, 133],
"violet red":[208, 32, 144],
"violetred":[208, 32, 144],
"magenta":[255, 0, 255],
"violet":[238, 130, 238],
"plum":[221, 160, 221],
"orchid":[218, 112, 214],
"medium orchid":[186, 85, 211],
"mediumorchid":[186, 85, 211],
"dark orchid":[153, 50, 204],
"darkorchid":[153, 50, 204],
"dark violet":[148, 0, 211],
"darkviolet":[148, 0, 211],
"blue violet":[138, 43, 226],
"blueviolet":[138, 43, 226],
"purple":[160, 32, 240],
"medium purple":[147, 112, 219],
"mediumpurple":[147, 112, 219],
"thistle":[216, 191, 216],
"snow1":[255, 250, 250],
"snow2":[238, 233, 233],
"snow3":[205, 201, 201],
"snow4":[139, 137, 137],
"seashell1":[255, 245, 238],
"seashell2":[238, 229, 222],
"seashell3":[205, 197, 191],
"seashell4":[139, 134, 130],
"antiquewhite1":[255, 239, 219],
"antiquewhite2":[238, 223, 204],
"antiquewhite3":[205, 192, 176],
"antiquewhite4":[139, 131, 120],
"bisque1":[255, 228, 196],
"bisque2":[238, 213, 183],
"bisque3":[205, 183, 158],
"bisque4":[139, 125, 107],
"peachpuff1":[255, 218, 185],
"peachpuff2":[238, 203, 173],
"peachpuff3":[205, 175, 149],
"peachpuff4":[139, 119, 101],
"navajowhite1":[255, 222, 173],
"navajowhite2":[238, 207, 161],
"navajowhite3":[205, 179, 139],
"navajowhite4":[139, 121, 94],
"lemonchiffon1":[255, 250, 205],
"lemonchiffon2":[238, 233, 191],
"lemonchiffon3":[205, 201, 165],
"lemonchiffon4":[139, 137, 112],
"cornsilk1":[255, 248, 220],
"cornsilk2":[238, 232, 205],
"cornsilk3":[205, 200, 177],
"cornsilk4":[139, 136, 120],
"ivory1":[255, 255, 240],
"ivory2":[238, 238, 224],
"ivory3":[205, 205, 193],
"ivory4":[139, 139, 131],
"honeydew1":[240, 255, 240],
"honeydew2":[224, 238, 224],
"honeydew3":[193, 205, 193],
"honeydew4":[131, 139, 131],
"lavenderblush1":[255, 240, 245],
"lavenderblush2":[238, 224, 229],
"lavenderblush3":[205, 193, 197],
"lavenderblush4":[139, 131, 134],
"mistyrose1":[255, 228, 225],
"mistyrose2":[238, 213, 210],
"mistyrose3":[205, 183, 181],
"mistyrose4":[139, 125, 123],
"azure1":[240, 255, 255],
"azure2":[224, 238, 238],
"azure3":[193, 205, 205],
"azure4":[131, 139, 139],
"slateblue1":[131, 111, 255],
"slateblue2":[122, 103, 238],
"slateblue3":[105, 89, 205],
"slateblue4":[71, 60, 139],
"royalblue1":[72, 118, 255],
"royalblue2":[67, 110, 238],
"royalblue3":[58, 95, 205],
"royalblue4":[39, 64, 139],
"blue1":[0, 0, 255],
"blue2":[0, 0, 238],
"blue3":[0, 0, 205],
"blue4":[0, 0, 139],
"dodgerblue1":[30, 144, 255],
"dodgerblue2":[28, 134, 238],
"dodgerblue3":[24, 116, 205],
"dodgerblue4":[16, 78, 139],
"steelblue1":[99, 184, 255],
"steelblue2":[92, 172, 238],
"steelblue3":[79, 148, 205],
"steelblue4":[54, 100, 139],
"deepskyblue1":[0, 191, 255],
"deepskyblue2":[0, 178, 238],
"deepskyblue3":[0, 154, 205],
"deepskyblue4":[0, 104, 139],
"skyblue1":[135, 206, 255],
"skyblue2":[126, 192, 238],
"skyblue3":[108, 166, 205],
"skyblue4":[74, 112, 139],
"lightskyblue1":[176, 226, 255],
"lightskyblue2":[164, 211, 238],
"lightskyblue3":[141, 182, 205],
"lightskyblue4":[96, 123, 139],
"slategray1":[198, 226, 255],
"slategray2":[185, 211, 238],
"slategray3":[159, 182, 205],
"slategray4":[108, 123, 139],
"lightsteelblue1":[202, 225, 255],
"lightsteelblue2":[188, 210, 238],
"lightsteelblue3":[162, 181, 205],
"lightsteelblue4":[110, 123, 139],
"lightblue1":[191, 239, 255],
"lightblue2":[178, 223, 238],
"lightblue3":[154, 192, 205],
"lightblue4":[104, 131, 139],
"lightcyan1":[224, 255, 255],
"lightcyan2":[209, 238, 238],
"lightcyan3":[180, 205, 205],
"lightcyan4":[122, 139, 139],
"paleturquoise1":[187, 255, 255],
"paleturquoise2":[174, 238, 238],
"paleturquoise3":[150, 205, 205],
"paleturquoise4":[102, 139, 139],
"cadetblue1":[152, 245, 255],
"cadetblue2":[142, 229, 238],
"cadetblue3":[122, 197, 205],
"cadetblue4":[83, 134, 139],
"turquoise1":[0, 245, 255],
"turquoise2":[0, 229, 238],
"turquoise3":[0, 197, 205],
"turquoise4":[0, 134, 139],
"cyan1":[0, 255, 255],
"cyan2":[0, 238, 238],
"cyan3":[0, 205, 205],
"cyan4":[0, 139, 139],
"darkslategray1":[151, 255, 255],
"darkslategray2":[141, 238, 238],
"darkslategray3":[121, 205, 205],
"darkslategray4":[82, 139, 139],
"aquamarine1":[127, 255, 212],
"aquamarine2":[118, 238, 198],
"aquamarine3":[102, 205, 170],
"aquamarine4":[69, 139, 116],
"darkseagreen1":[193, 255, 193],
"darkseagreen2":[180, 238, 180],
"darkseagreen3":[155, 205, 155],
"darkseagreen4":[105, 139, 105],
"seagreen1":[84, 255, 159],
"seagreen2":[78, 238, 148],
"seagreen3":[67, 205, 128],
"seagreen4":[46, 139, 87],
"palegreen1":[154, 255, 154],
"palegreen2":[144, 238, 144],
"palegreen3":[124, 205, 124],
"palegreen4":[84, 139, 84],
"springgreen1":[0, 255, 127],
"springgreen2":[0, 238, 118],
"springgreen3":[0, 205, 102],
"springgreen4":[0, 139, 69],
"green1":[0, 255, 0],
"green2":[0, 238, 0],
"green3":[0, 205, 0],
"green4":[0, 139, 0],
"chartreuse1":[127, 255, 0],
"chartreuse2":[118, 238, 0],
"chartreuse3":[102, 205, 0],
"chartreuse4":[69, 139, 0],
"olivedrab1":[192, 255, 62],
"olivedrab2":[179, 238, 58],
"olivedrab3":[154, 205, 50],
"olivedrab4":[105, 139, 34],
"darkolivegreen1":[202, 255, 112],
"darkolivegreen2":[188, 238, 104],
"darkolivegreen3":[162, 205, 90],
"darkolivegreen4":[110, 139, 61],
"khaki1":[255, 246, 143],
"khaki2":[238, 230, 133],
"khaki3":[205, 198, 115],
"khaki4":[139, 134, 78],
"lightgoldenrod1":[255, 236, 139],
"lightgoldenrod2":[238, 220, 130],
"lightgoldenrod3":[205, 190, 112],
"lightgoldenrod4":[139, 129, 76],
"lightyellow1":[255, 255, 224],
"lightyellow2":[238, 238, 209],
"lightyellow3":[205, 205, 180],
"lightyellow4":[139, 139, 122],
"yellow1":[255, 255, 0],
"yellow2":[238, 238, 0],
"yellow3":[205, 205, 0],
"yellow4":[139, 139, 0],
"gold1":[255, 215, 0],
"gold2":[238, 201, 0],
"gold3":[205, 173, 0],
"gold4":[139, 117, 0],
"goldenrod1":[255, 193, 37],
"goldenrod2":[238, 180, 34],
"goldenrod3":[205, 155, 29],
"goldenrod4":[139, 105, 20],
"darkgoldenrod1":[255, 185, 15],
"darkgoldenrod2":[238, 173, 14],
"darkgoldenrod3":[205, 149, 12],
"darkgoldenrod4":[139, 101, 8],
"rosybrown1":[255, 193, 193],
"rosybrown2":[238, 180, 180],
"rosybrown3":[205, 155, 155],
"rosybrown4":[139, 105, 105],
"indianred1":[255, 106, 106],
"indianred2":[238, 99, 99],
"indianred3":[205, 85, 85],
"indianred4":[139, 58, 58],
"sienna1":[255, 130, 71],
"sienna2":[238, 121, 66],
"sienna3":[205, 104, 57],
"sienna4":[139, 71, 38],
"burlywood1":[255, 211, 155],
"burlywood2":[238, 197, 145],
"burlywood3":[205, 170, 125],
"burlywood4":[139, 115, 85],
"wheat1":[255, 231, 186],
"wheat2":[238, 216, 174],
"wheat3":[205, 186, 150],
"wheat4":[139, 126, 102],
"tan1":[255, 165, 79],
"tan2":[238, 154, 73],
"tan3":[205, 133, 63],
"tan4":[139, 90, 43],
"chocolate1":[255, 127, 36],
"chocolate2":[238, 118, 33],
"chocolate3":[205, 102, 29],
"chocolate4":[139, 69, 19],
"firebrick1":[255, 48, 48],
"firebrick2":[238, 44, 44],
"firebrick3":[205, 38, 38],
"firebrick4":[139, 26, 26],
"brown1":[255, 64, 64],
"brown2":[238, 59, 59],
"brown3":[205, 51, 51],
"brown4":[139, 35, 35],
"salmon1":[255, 140, 105],
"salmon2":[238, 130, 98],
"salmon3":[205, 112, 84],
"salmon4":[139, 76, 57],
"lightsalmon1":[255, 160, 122],
"lightsalmon2":[238, 149, 114],
"lightsalmon3":[205, 129, 98],
"lightsalmon4":[139, 87, 66],
"orange1":[255, 165, 0],
"orange2":[238, 154, 0],
"orange3":[205, 133, 0],
"orange4":[139, 90, 0],
"darkorange1":[255, 127, 0],
"darkorange2":[238, 118, 0],
"darkorange3":[205, 102, 0],
"darkorange4":[139, 69, 0],
"coral1":[255, 114, 86],
"coral2":[238, 106, 80],
"coral3":[205, 91, 69],
"coral4":[139, 62, 47],
"tomato1":[255, 99, 71],
"tomato2":[238, 92, 66],
"tomato3":[205, 79, 57],
"tomato4":[139, 54, 38],
"orangered1":[255, 69, 0],
"orangered2":[238, 64, 0],
"orangered3":[205, 55, 0],
"orangered4":[139, 37, 0],
"red1":[255, 0, 0],
"red2":[238, 0, 0],
"red3":[205, 0, 0],
"red4":[139, 0, 0],
"deeppink1":[255, 20, 147],
"deeppink2":[238, 18, 137],
"deeppink3":[205, 16, 118],
"deeppink4":[139, 10, 80],
"hotpink1":[255, 110, 180],
"hotpink2":[238, 106, 167],
"hotpink3":[205, 96, 144],
"hotpink4":[139, 58, 98],
"pink1":[255, 181, 197],
"pink2":[238, 169, 184],
"pink3":[205, 145, 158],
"pink4":[139, 99, 108],
"lightpink1":[255, 174, 185],
"lightpink2":[238, 162, 173],
"lightpink3":[205, 140, 149],
"lightpink4":[139, 95, 101],
"palevioletred1":[255, 130, 171],
"palevioletred2":[238, 121, 159],
"palevioletred3":[205, 104, 137],
"palevioletred4":[139, 71, 93],
"maroon1":[255, 52, 179],
"maroon2":[238, 48, 167],
"maroon3":[205, 41, 144],
"maroon4":[139, 28, 98],
"violetred1":[255, 62, 150],
"violetred2":[238, 58, 140],
"violetred3":[205, 50, 120],
"violetred4":[139, 34, 82],
"magenta1":[255, 0, 255],
"magenta2":[238, 0, 238],
"magenta3":[205, 0, 205],
"magenta4":[139, 0, 139],
"orchid1":[255, 131, 250],
"orchid2":[238, 122, 233],
"orchid3":[205, 105, 201],
"orchid4":[139, 71, 137],
"plum1":[255, 187, 255],
"plum2":[238, 174, 238],
"plum3":[205, 150, 205],
"plum4":[139, 102, 139],
"mediumorchid1":[224, 102, 255],
"mediumorchid2":[209, 95, 238],
"mediumorchid3":[180, 82, 205],
"mediumorchid4":[122, 55, 139],
"darkorchid1":[191, 62, 255],
"darkorchid2":[178, 58, 238],
"darkorchid3":[154, 50, 205],
"darkorchid4":[104, 34, 139],
"purple1":[155, 48, 255],
"purple2":[145, 44, 238],
"purple3":[125, 38, 205],
"purple4":[85, 26, 139],
"mediumpurple1":[171, 130, 255],
"mediumpurple2":[159, 121, 238],
"mediumpurple3":[137, 104, 205],
"mediumpurple4":[93, 71, 139],
"thistle1":[255, 225, 255],
"thistle2":[238, 210, 238],
"thistle3":[205, 181, 205],
"thistle4":[139, 123, 139],
"gray0":[0, 0, 0],
"grey0":[0, 0, 0],
"gray1":[3, 3, 3],
"grey1":[3, 3, 3],
"gray2":[5, 5, 5],
"grey2":[5, 5, 5],
"gray3":[8, 8, 8],
"grey3":[8, 8, 8],
"gray4":[10, 10, 10],
"grey4":[10, 10, 10],
"gray5":[13, 13, 13],
"grey5":[13, 13, 13],
"gray6":[15, 15, 15],
"grey6":[15, 15, 15],
"gray7":[18, 18, 18],
"grey7":[18, 18, 18],
"gray8":[20, 20, 20],
"grey8":[20, 20, 20],
"gray9":[23, 23, 23],
"grey9":[23, 23, 23],
"gray10":[26, 26, 26],
"grey10":[26, 26, 26],
"gray11":[28, 28, 28],
"grey11":[28, 28, 28],
"gray12":[31, 31, 31],
"grey12":[31, 31, 31],
"gray13":[33, 33, 33],
"grey13":[33, 33, 33],
"gray14":[36, 36, 36],
"grey14":[36, 36, 36],
"gray15":[38, 38, 38],
"grey15":[38, 38, 38],
"gray16":[41, 41, 41],
"grey16":[41, 41, 41],
"gray17":[43, 43, 43],
"grey17":[43, 43, 43],
"gray18":[46, 46, 46],
"grey18":[46, 46, 46],
"gray19":[48, 48, 48],
"grey19":[48, 48, 48],
"gray20":[51, 51, 51],
"grey20":[51, 51, 51],
"gray21":[54, 54, 54],
"grey21":[54, 54, 54],
"gray22":[56, 56, 56],
"grey22":[56, 56, 56],
"gray23":[59, 59, 59],
"grey23":[59, 59, 59],
"gray24":[61, 61, 61],
"grey24":[61, 61, 61],
"gray25":[64, 64, 64],
"grey25":[64, 64, 64],
"gray26":[66, 66, 66],
"grey26":[66, 66, 66],
"gray27":[69, 69, 69],
"grey27":[69, 69, 69],
"gray28":[71, 71, 71],
"grey28":[71, 71, 71],
"gray29":[74, 74, 74],
"grey29":[74, 74, 74],
"gray30":[77, 77, 77],
"grey30":[77, 77, 77],
"gray31":[79, 79, 79],
"grey31":[79, 79, 79],
"gray32":[82, 82, 82],
"grey32":[82, 82, 82],
"gray33":[84, 84, 84],
"grey33":[84, 84, 84],
"gray34":[87, 87, 87],
"grey34":[87, 87, 87],
"gray35":[89, 89, 89],
"grey35":[89, 89, 89],
"gray36":[92, 92, 92],
"grey36":[92, 92, 92],
"gray37":[94, 94, 94],
"grey37":[94, 94, 94],
"gray38":[97, 97, 97],
"grey38":[97, 97, 97],
"gray39":[99, 99, 99],
"grey39":[99, 99, 99],
"gray40":[102, 102, 102],
"grey40":[102, 102, 102],
"gray41":[105, 105, 105],
"grey41":[105, 105, 105],
"gray42":[107, 107, 107],
"grey42":[107, 107, 107],
"gray43":[110, 110, 110],
"grey43":[110, 110, 110],
"gray44":[112, 112, 112],
"grey44":[112, 112, 112],
"gray45":[115, 115, 115],
"grey45":[115, 115, 115],
"gray46":[117, 117, 117],
"grey46":[117, 117, 117],
"gray47":[120, 120, 120],
"grey47":[120, 120, 120],
"gray48":[122, 122, 122],
"grey48":[122, 122, 122],
"gray49":[125, 125, 125],
"grey49":[125, 125, 125],
"gray50":[127, 127, 127],
"grey50":[127, 127, 127],
"gray51":[130, 130, 130],
"grey51":[130, 130, 130],
"gray52":[133, 133, 133],
"grey52":[133, 133, 133],
"gray53":[135, 135, 135],
"grey53":[135, 135, 135],
"gray54":[138, 138, 138],
"grey54":[138, 138, 138],
"gray55":[140, 140, 140],
"grey55":[140, 140, 140],
"gray56":[143, 143, 143],
"grey56":[143, 143, 143],
"gray57":[145, 145, 145],
"grey57":[145, 145, 145],
"gray58":[148, 148, 148],
"grey58":[148, 148, 148],
"gray59":[150, 150, 150],
"grey59":[150, 150, 150],
"gray60":[153, 153, 153],
"grey60":[153, 153, 153],
"gray61":[156, 156, 156],
"grey61":[156, 156, 156],
"gray62":[158, 158, 158],
"grey62":[158, 158, 158],
"gray63":[161, 161, 161],
"grey63":[161, 161, 161],
"gray64":[163, 163, 163],
"grey64":[163, 163, 163],
"gray65":[166, 166, 166],
"grey65":[166, 166, 166],
"gray66":[168, 168, 168],
"grey66":[168, 168, 168],
"gray67":[171, 171, 171],
"grey67":[171, 171, 171],
"gray68":[173, 173, 173],
"grey68":[173, 173, 173],
"gray69":[176, 176, 176],
"grey69":[176, 176, 176],
"gray70":[179, 179, 179],
"grey70":[179, 179, 179],
"gray71":[181, 181, 181],
"grey71":[181, 181, 181],
"gray72":[184, 184, 184],
"grey72":[184, 184, 184],
"gray73":[186, 186, 186],
"grey73":[186, 186, 186],
"gray74":[189, 189, 189],
"grey74":[189, 189, 189],
"gray75":[191, 191, 191],
"grey75":[191, 191, 191],
"gray76":[194, 194, 194],
"grey76":[194, 194, 194],
"gray77":[196, 196, 196],
"grey77":[196, 196, 196],
"gray78":[199, 199, 199],
"grey78":[199, 199, 199],
"gray79":[201, 201, 201],
"grey79":[201, 201, 201],
"gray80":[204, 204, 204],
"grey80":[204, 204, 204],
"gray81":[207, 207, 207],
"grey81":[207, 207, 207],
"gray82":[209, 209, 209],
"grey82":[209, 209, 209],
"gray83":[212, 212, 212],
"grey83":[212, 212, 212],
"gray84":[214, 214, 214],
"grey84":[214, 214, 214],
"gray85":[217, 217, 217],
"grey85":[217, 217, 217],
"gray86":[219, 219, 219],
"grey86":[219, 219, 219],
"gray87":[222, 222, 222],
"grey87":[222, 222, 222],
"gray88":[224, 224, 224],
"grey88":[224, 224, 224],
"gray89":[227, 227, 227],
"grey89":[227, 227, 227],
"gray90":[229, 229, 229],
"grey90":[229, 229, 229],
"gray91":[232, 232, 232],
"grey91":[232, 232, 232],
"gray92":[235, 235, 235],
"grey92":[235, 235, 235],
"gray93":[237, 237, 237],
"grey93":[237, 237, 237],
"gray94":[240, 240, 240],
"grey94":[240, 240, 240],
"gray95":[242, 242, 242],
"grey95":[242, 242, 242],
"gray96":[245, 245, 245],
"grey96":[245, 245, 245],
"gray97":[247, 247, 247],
"grey97":[247, 247, 247],
"gray98":[250, 250, 250],
"grey98":[250, 250, 250],
"gray99":[252, 252, 252],
"grey99":[252, 252, 252],
"gray100":[255, 255, 255],
"grey100":[255, 255, 255],
"dark grey":[169, 169, 169],
"darkgrey":[169, 169, 169],
"dark gray":[169, 169, 169],
"darkgray":[169, 169, 169],
"dark blue":[0, 0, 139],
"darkblue":[0, 0, 139],
"dark cyan":[0, 139, 139],
"darkcyan":[0, 139, 139],
"dark magenta":[139, 0, 139],
"darkmagenta":[139, 0, 139],
"dark red":[139, 0, 0],
"darkred":[139, 0, 0],
"light green":[144, 238, 144],
"lightgreen":[144, 238, 144],
"olive":[128, 128, 0],
"teal":[0, 128, 128]}
