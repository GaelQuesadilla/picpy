from PIL import Image, ImageTk
import numpy as np
from pathlib import Path
from typing import Optional, Deque, Callable, List, Tuple
from collections import deque
from picpy.utils.logger import logger


def default_listener(): return logger.debug("Listener activado")


class ImageModel:
    """Clase modelo de la imagen
    """

    def __init__(self, image: Optional[Image.Image] = None, max_history: int = 3):
        """Clase modelo para guardar los

        Parameters
        ----------
        image : Optional[Image.Image], optional
            Imagen inicial, por defecto None
        max_history : int, optional
            Cantidad máxima de imágenes del historial, por defecto 3

        Raises
        ------
        ValueError
            Cuando el historial máximo sea menor a 1
        """

        if max_history < 1:
            raise ValueError("El tamaño historial no puede ser menor que uno")

        self._original_image: np.ndarray | None = None
        self._history: Deque[np.ndarray] = deque(maxlen=5)
        self.path: Path | str
        self._listeners: List[Callable[[], None]] = []
        self.add_listener(default_listener)

    @property
    def has_image(self) -> bool:
        """Indica si hay al menos un valor en el historial

        Returns
        -------
        bool
            True si el historial contiene más de una imagen en el historial; False en caso contrario
        """
        return len(self._history) > 0

    @property
    def current_array(self) -> np.ndarray | None:
        """Devuelve una copia de la matriz de la imagen actual

        Returns
        ------- 
        np.ndarray | None
            Copia de la matriz de la imagen actual; None si no hay ninguna imagen
        """
        if not self.has_image:
            return None
        return self._history[0].copy()

    def add_listener(self, listener: Callable[[], None]) -> None:
        """Añade un Listener que escuchará cuando una imagen cambie

        Parameters
        ----------
        listener : Callable[[], None]
            Listener a ser añadido
        """
        if listener in self._listeners:
            return
        self._listeners.append(listener)

    def notify_listeners(self) -> None:
        """Notifica a los Listeners
        """
        for listener in self._listeners:
            listener()

    def load_image(self, path: Path | str):
        """Carga una imagen al modelo y la establece como valor inicial


        Parameters
        ----------
        path : Path | str
            Ruta de la imagen a cargar
        """

        if isinstance(path, Path):
            path = path.absolute()
        self.path = path
        image = Image.open(path)
        image_array = np.asarray(image.convert("RGB"))
        self._history.clear()
        self._push_state(image_array)
        self._original_image = self._history[0].copy()

    def _push_state(self, image_array: np.ndarray):
        self._history.appendleft(self._to_float32(image_array))
        self.notify_listeners()

    @staticmethod
    def _to_float32(array: np.ndarray) -> np.typing.NDArray[np.float32]:
        """Convierte los datos de una matriz en flotante de 32 bits

        Parameters
        ----------
        array : np.ndarray
            La matriz original

        Returns
        -------
        np.typing.NDArray[np.float32]
            Una nueva matriz con datos en un rango [0,1]
        """
        if array.dtype == np.float32:
            return np.copy(array)

        return array.astype(np.float32) / 255.0

    @staticmethod
    def _to_uint8(array: np.ndarray) -> np.typing.NDArray[np.uint8]:
        """Convierte los datos de una matriz en uint8

        Parameters
        ----------
        array : np.ndarray
            La matriz original

        Returns
        -------
        np.typing.NDArray[np.uint8]
            Una nueva matriz de datos enteros de 8 bits
        """
        if array.dtype == np.int8:
            return np.copy(array)

        return (ImageModel._normalize(array)*255).astype(np.uint8)

    @staticmethod
    def _normalize(array: np.typing.NDArray[np.float32 | np.float16]) -> np.ndarray:
        """_summary_

        Parameters
        ----------
        array : np.typing.NDArray[np.float32  |  np.float16]
            La matriz original

        Returns
        -------
        np.ndarray
            Una nueva matriz con datos en un rango [0,1]
        """
        return np.clip(array, 0.0, 1.0)

    def get_current_as_pil(self, size: Tuple[int, int] | None = None) -> Image.Image | None:
        """Convierte la última imagen del historial en un objeto PIL

        Parameters
        ----------
        size : Tuple[int, int] | None, optional
            El tamaño de la nueva imagen, por defecto None

        Returns
        -------
        Image.Image | None
            La imagen PIL
        """
        array = self.current_array
        if array is None:
            logger.warning("No hay ninguna imagen cargada")
            return None

        array = self._normalize(array)
        pil_array = self._to_uint8(array)
        image = Image.fromarray(pil_array)
        if not size is None:
            image = image.resize(size)

        return image

    def get_current_as_tk(self, size: Tuple[int, int] | None = None) -> ImageTk.PhotoImage | None:
        """Convierte la última imagen del historial en un objeto compatible con TK

        Parameters
        ----------
        size : Tuple[int, int] | None, optional
            El tamaño de la nueva imagen, por defecto None

        Returns
        -------
        Image.Image | None
            La Imagen compatible con TK
        """
        image = self.get_current_as_pil(size=size)
        if image is None:
            logger.warning("No hay ninguna imagen cargada")
            return None
        image_tk = ImageTk.PhotoImage(image=image)

        return image_tk

    def apply_operation(self, operation: Callable[[np.ndarray], np.ndarray], *args, **kwargs) -> None:
        """Aplica una operación a la imagen y actualiza su estado

        Parameters
        ----------
        operation : Callable[[np.ndarray], np.ndarray
            Función a ejecutar sobre la matriz de datos

        Raises
        ------
        RuntimeError
            Cuando no hay ninguna imagen cargada
        """
        if self.current_array is None:
            raise RuntimeError("No hay ninguna imagen cargada")

        result = operation(self.current_array, *args, **kwargs)

        self._push_state(result)
