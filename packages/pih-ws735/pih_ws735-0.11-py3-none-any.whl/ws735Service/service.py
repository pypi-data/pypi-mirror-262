import ipih

from pih import A
from ws735Service.const import SD

SC = A.CT_SC


def start(as_standalone: bool = False) -> None:
    
    if A.U.for_service(SD):

        from typing import Any
        from pih.tools import ParameterList
        from PIL import Image, ImageWin
        import win32ui
        import win32print

        def service_call_handler(sc: SC, pl: ParameterList) -> Any:  
            if sc == SC.print_image:
                HORZRES = 8
                VERTRES = 10
                PHYSICALWIDTH = 110
                PHYSICALHEIGHT = 111
                printer_name: str = "qr_printer"
                printer_status: int = win32print.GetPrinter(win32print.OpenPrinter(printer_name))[13]
                if (printer_status & 0x00000400) >> 10:
                    return False
                file_name: str = pl.next()
                hDC = win32ui.CreateDC()
                hDC.CreatePrinterDC(printer_name)
                printable_area = hDC.GetDeviceCaps(HORZRES), hDC.GetDeviceCaps(VERTRES)
                printer_size = hDC.GetDeviceCaps(
                    PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)
                bmp = Image.open(file_name)
                if bmp.size[0] > bmp.size[1]:
                    bmp = bmp.rotate(90)
                ratios = [1.0 * printable_area[0] / bmp.size[0],
                        1.0 * printable_area[1] / bmp.size[1]]
                scale: float = min(ratios)
                hDC.StartDoc(file_name)
                hDC.StartPage()
                dib = ImageWin.Dib(bmp)
                scaled_width, scaled_height = [int(scale * i) for i in bmp.size]
                x1 = int((printer_size[0] - scaled_width) / 2)
                y1 = int((printer_size[1] - scaled_height) / 2)
                x2 = x1 + scaled_width
                y2 = y1 + scaled_height
                dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))
                hDC.EndPage()
                hDC.EndDoc()
                hDC.DeleteDC()
                return True
            return None

        A.SRV_A.serve(SD, service_call_handler, as_standalone=as_standalone)
    
if __name__ == "__main__":
    start()
