#!/usr/bin/env python

import gst
import Image

class ImageSink(gst.Bin):
    '''
    Pulls buffers from the Gstreamer pipeline when they become available and passes
    them to registered callback functions.  The raw buffer is converted to a PIL
    Image before it gets handed off.
    '''

    DROP_BUFFERS = True
    MAX_BUFFERS = 10
    callbacks = []

    def __init__(self, size=(320,240), framerate=10, bpp=24, depth=24):
        '''
        Initializes the C{ImageSink} class which is a sub-class of the
        Gstreamer Bin class.  This class can more-or-less be treated like a
        Gstreamer element and can be inserted into the pipeline as such.

        @param  size:       The size of frames to grab off the pipeline as a
                            tuple of two ints, width and height, ie (320,240).
        @type   size:       Tuple
        @param  framerate:  The number of frames per second to get frames at.
        @type   framerate:  Integer
        @param  bpp:        The number of bits per pixel of the frames.
        @type   bpp:        Integer
        @param  depth:      Color depth of the frames.
        @type   depth:      Integer
        '''
        gst.Bin.__init__(self)

        self._size = size
        self._framerate = framerate
        self._bpp = bpp
        self._depth = depth

        queue = gst.element_factory_make('queue', 'queue_pis')
        scale = gst.element_factory_make('videoscale', 'scale_pis')
        rate = gst.element_factory_make('videorate', 'rate_pis')
        color = gst.element_factory_make('ffmpegcolorspace', 'color_pis')
        filter = gst.element_factory_make('capsfilter', 'filter_pis')
        sink = gst.element_factory_make('appsink', 'appsink_pis')

        caps = gst.caps_from_string('''
            video/x-raw-rgb,
            bpp=%d, depth=%d,
            width=%d, height=%d,
            framerate=%d/1
            ''' %
            (self._bpp, self._depth,
            self._size[0], self._size[1],
            self._framerate))

        filter.set_property('caps', caps)

        sink.set_property('emit-signals', True)
        sink.set_property('drop', self.DROP_BUFFERS)
        sink.set_property('max-buffers', self.MAX_BUFFERS)
        sink.connect('new-buffer', self.on_new_buffer)

        self.add(queue, scale, rate, color, filter, sink)
        gst.element_link_many(queue, scale, rate, color, filter, sink)

        pad = queue.get_pad('sink')
        ghostpad = gst.GhostPad('sink', pad)
        self.add_pad(ghostpad)

        self.set_state(gst.STATE_NULL)

    def _update_caps(self):
        '''
        Builds a new C{gst.Caps} instance from a string containing this
        class's relevant attributes (size, framerate, etc).  This method
        gets called whenever one of the properties gets updated.
        '''
        caps = gst.caps_from_string('''
            video/x-raw-rgb,
            bpp=%d, depth=%d,
            width=%d, height=%d,
            framerate=%d/1
            ''' %
            (self._bpp, self._depth,
            self._size[0], self._size[1],
            self._framerate))
        filter = self.get_by_name('filter_pis')
        filter.set_property('caps', caps)

    def set_framerate(self, value):
        self._framerate = value
        self._update_caps()
    def get_framerate(self): return self._framerate
    framerate = property(get_framerate, set_framerate,
        'The number of frames per second to get frames at.')

    def set_size(self, value):
        self._size = value
        self._update_caps()
    def get_size(self): return self._size
    size = property(get_size, set_size,
        '''The size of frames to grab off the pipeline as a
        tuple of two ints, width and height, ie (320,240).''')

    def set_bpp(self, value):
        self._bpp = value
        self._update_caps()
    def get_bpp(self): return self._bpp
    bpp = property(get_bpp, set_bpp,
        'The number of bits per pixel of the frames.')

    def set_depth(self, value):
        self._depth = value
        self._update_caps()
    def get_depth(self): return self._depth
    depth = property(get_size, set_size, 'Color depth of the frames.')

    def start(self):
        '''
        Enable grabbing of frames from the pipeline.  This doesn't change
        the state of the elements, everything still runs except that none of
        the callbacks will be fired and no buffers will be read from the
        pipeline.
        '''
        appsink = self.get_by_name('appsink_pis')
        appsink.set_property('emit-signals', True)

    def stop(self):
        '''
        Disables grabbing of frames from the pipeline.  See start().
        '''
        appsink = self.get_by_name('appsink_pis')
        appsink.set_property('emit-signals', False)

    def connect(self, cbfunc, *args):
        '''
        Add C{cbfunc} to the list of callbacks to call when a new frame/image
        is ready.  C{cbfunc} should take one argument, the PIL Image created
        from the buffer that was read.

        @param  cbfunc: The callback function to add to C{callbacks} list.
        @type   cbfunc: Function
        '''
        if cbfunc not in self.callbacks:
            self.callbacks.append((cbfunc, args))

    def disconnect(self, cbfunc):
        '''
        Removes C{cbfunc} from the list of callbacks to call when a new
        frame/image is ready.

        @param  cbfunc: The callback function to remove from C{callbacks} list.
        @type   cbfunc: Function
        '''
        if cbfunc in self.callbacks:
            for cb in self.callbacks:
                if cb[0] == cbfunc: self.callbacks.remove(cb)

    def on_new_buffer(self, appsink):
        '''
        Callback which gets called when the appsink element sends a 'new-buffer'
        signal indicating that a buffer is ready on the bus.  The buffer is
        converted to a PIL Image and passed as an argument to each of the
        callback functions which are "subscribed/connected".

        @param  appsink:    The Gstreamer element that fired the 'new-buffer'
                            signal.
        @type   appsink:    gst.Element
        '''
        try:
            buffer = appsink.emit('pull-buffer')
            img = Image.fromstring('RGB', self.size, buffer)
            # call all of the "subscribed/connected" callback functions
            for cb in self.callbacks: cb[0](self, img, *cb[1])
        except IOError: pass


#-------------------------------------------------------------------------------
# test script
# -----------
# Very basic, launches a GTK window with an Image widget.  Attaches a callback
# to the PythonImageSink bin/element, and within callback, updates the Image
# widget with the last image (converted to a pixbuf).
#-------------------------------------------------------------------------------
if __name__ == '__main__':

    from cStringIO import StringIO
    import gtk
    import gobject
    gobject.threads_init()

    def update_window_image(element, img, widget):
        pixbuf = image_to_pixbuf(img)
        widget[0].set_from_pixbuf(pixbuf)

    def image_to_pixbuf (image):
        file = StringIO ()
        image.save (file, 'ppm')
        contents = file.getvalue()
        file.close ()
        loader = gtk.gdk.PixbufLoader ('pnm')
        loader.write (contents, len (contents))
        pixbuf = loader.get_pixbuf ()
        loader.close ()
        return pixbuf

    wnd = gtk.Window()
    wnd.connect('destroy', gtk.main_quit)
    img = gtk.Image()
    wnd.add(img)
    wnd.show_all()

    p = gst.Pipeline('pl0')

    #src = gst.element_factory_make('v4l2src', 'src')
    #src.set_property('device', '/dev/video2')
    src = gst.element_factory_make('videotestsrc', 'src')
#    src = gst.element_factory_make("autovideosrc", "src")
#   src.set_property("uri", "file://" + "/home/black/test.avi")
#    src.set_property('pattern', 'snow')

    pis = ImageSink()

    pis.size = (640, 480)
    pis.framerate = 30

    p.add(src, pis)
    gst.element_link_many(src, pis)

    pis.connect(update_window_image, [img])

    p.set_state(gst.STATE_PLAYING)

    gtk.main()

