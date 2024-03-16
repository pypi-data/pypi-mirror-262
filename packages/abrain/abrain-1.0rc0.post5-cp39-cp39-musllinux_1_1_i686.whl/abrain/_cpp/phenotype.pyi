"""
Docstring for phenotype submodule
"""
from __future__ import annotations
import _cpp.genotype
import typing
__all__ = ['ANN', 'CPPN', 'Point']
class ANN:
    """
    3D Artificial Neural Network produced through Evolvable Substrate Hyper-NEAT
    """
    class IBuffer:
        """
        Specialized, fixed-size buffer for the neural inputs (write-only)
        """
        def __len__(self) -> int:
            """
            Return the number of expected inputs
            """
        @typing.overload
        def __setitem__(self, arg0: int, arg1: float) -> None:
            """
            Assign an element
            """
        @typing.overload
        def __setitem__(self, arg0: slice, arg1: typing.Iterable) -> None:
            ...
    class Neuron:
        """
        Atomic computational unit of an ANN
        """
        class Link:
            """
            An incoming neural connection
            """
            def src(self) -> ANN.Neuron:
                """
                Return a reference to the source neuron
                """
            @property
            def weight(self) -> float:
                """
                Connection weight (see attr:`Config.annWeightScale`)
                """
        class Type:
            """
            Members:
            
              I : Input (receiving data)
            
              H : Hidden (processing data)
            
              O : Output (producing data)
            """
            H: typing.ClassVar[ANN.Neuron.Type]  # value = <Type.H: 2>
            I: typing.ClassVar[ANN.Neuron.Type]  # value = <Type.I: 0>
            O: typing.ClassVar[ANN.Neuron.Type]  # value = <Type.O: 1>
            __members__: typing.ClassVar[dict[str, ANN.Neuron.Type]]  # value = {'I': <Type.I: 0>, 'H': <Type.H: 2>, 'O': <Type.O: 1>}
            def __eq__(self, other: typing.Any) -> bool:
                ...
            def __getstate__(self) -> int:
                ...
            def __hash__(self) -> int:
                ...
            def __index__(self) -> int:
                ...
            def __init__(self, value: int) -> None:
                ...
            def __int__(self) -> int:
                ...
            def __ne__(self, other: typing.Any) -> bool:
                ...
            def __repr__(self) -> str:
                ...
            def __setstate__(self, state: int) -> None:
                ...
            def __str__(self) -> str:
                ...
            @property
            def name(self) -> str:
                ...
            @property
            def value(self) -> int:
                ...
        def links(self) -> list[ANN.Neuron.Link]:
            """
            Return the list of inputs connections
            """
        @property
        def bias(self) -> float:
            """
            Neural bias
            """
        @property
        def depth(self) -> int:
            """
            Depth in the neural network
            """
        @property
        def flags(self) -> int:
            """
            Stimuli-dependent flags (for modularization)
            """
        @property
        def pos(self) -> Point:
            """
            Position in the 3D substrate
            """
        @property
        def type(self) -> ANN.Neuron.Type:
            """
            Neuron role (see :class:`Type`)
            """
        @property
        def value(self) -> float:
            """
            Current activation value
            """
    class Neurons:
        """
        Wrapper for the C++ neurons container
        """
        def __iter__(self) -> typing.Iterator:
            ...
        def __len__(self) -> int:
            ...
    class OBuffer:
        """
        Specialized, fixed-size buffer for the neural outputs (read-only)
        """
        @typing.overload
        def __getitem__(self, arg0: int) -> float:
            """
            Access an element
            """
        @typing.overload
        def __getitem__(self, arg0: slice) -> list:
            ...
        def __len__(self) -> int:
            """
            Return the number of expected outputs
            """
        @property
        def __iter__(self) -> None:
            """
            Cannot be iterated. Use direct access instead.
            """
    class Stats:
        """
        Contains various statistics about an ANN
        """
        def dict(self) -> dict:
            """
            Return the stats as Python dictionary
            """
        @property
        def axons(self) -> float:
            """
            Total length of the connections
            """
        @property
        def density(self) -> float:
            """
            Ratio of expressed connections
            """
        @property
        def depth(self) -> int:
            """
            Maximal depth of the neural network
            """
        @property
        def edges(self) -> int:
            """
            Number of connections
            """
        @property
        def hidden(self) -> int:
            """
            Number of hidden neurons
            """
        @property
        def iterations(self) -> int:
            """
            H -> H iterations before convergence
            """
    @staticmethod
    def build(inputs: list[Point], outputs: list[Point], genome: _cpp.genotype.CPPNData) -> ANN:
        """
        Create an ANN via ES-HyperNEAT
        
        The ANN has inputs/outputs at specified coordinates.
        A CPPN is instantiated from the provided genome and used
        to query connections weight, existence and to discover
        hidden neurons locations
        
        :param inputs: coordinates of the input neurons on the substrate
        :param outputs: coordinates of the output neurons on the substrate
        :param genome: genome describing a cppn (see :class:`abrain.Genome`,
                                                :class:`CPPN`)
        
        .. seealso:: :ref:`usage-basics-ann`
        """
    def __call__(self, inputs: ANN.IBuffer, outputs: ANN.OBuffer, substeps: int = 1) -> None:
        """
        Execute a computational step
        
        Assigns provided input values to corresponding input neurons in the same order
        as when created (see build). Returns output values as computed.
        If not otherwise specified, a single computational substep is executed. If need
        be (e.g. large network, fast response required) you can requested for multiple
        sequential execution in one call
        
        :param inputs: provided analog values for the input neurons
        :param outputs: computed analog values for the output neurons
        :param substeps: number of sequential executions
        
        .. seealso:: :ref:`usage-basics-ann`
        """
    def __init__(self) -> None:
        ...
    def buffers(self) -> tuple[ANN.IBuffer, ANN.OBuffer]:
        """
        Return the ann's I/O buffers as a tuple
        """
    def empty(self, strict: bool = False) -> bool:
        """
        Whether the ANN contains neurons/connections
        
        :param strict: whether perceptrons count as empty (true) or not (false)
        
        .. seealso:: `Config::allowPerceptrons`
        """
    def ibuffer(self) -> ANN.IBuffer:
        """
        Return a reference to the neural inputs buffer
        """
    def neuronAt(self, pos: Point) -> ANN.Neuron:
        """
        Query an individual neuron
        """
    def neurons(self) -> ANN.Neurons:
        """
        Provide read-only access to the underlying neurons
        """
    def obuffer(self) -> ANN.OBuffer:
        """
        Return a reference to the neural outputs buffer
        """
    def perceptron(self) -> bool:
        """
        Whether this ANN is a perceptron
        """
    def reset(self) -> None:
        """
        Resets internal state to null (0)
        """
    def stats(self) -> ANN.Stats:
        """
        Return associated stats (connections, depth...)
        """
class CPPN:
    """
    Middle-man between the descriptive :class:`Genome` and the callable :class:`ANN`
    """
    class Output:
        """
        Members:
        
          Weight
        
          LEO
        
          Bias
        """
        Bias: typing.ClassVar[CPPN.Output]  # value = <Output.Bias: 2>
        LEO: typing.ClassVar[CPPN.Output]  # value = <Output.LEO: 1>
        Weight: typing.ClassVar[CPPN.Output]  # value = <Output.Weight: 0>
        __members__: typing.ClassVar[dict[str, CPPN.Output]]  # value = {'Weight': <Output.Weight: 0>, 'LEO': <Output.LEO: 1>, 'Bias': <Output.Bias: 2>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class Outputs:
        """
        Output communication buffer for the CPPN
        """
        def __getitem__(self, arg0: int) -> float:
            ...
        def __init__(self) -> None:
            ...
        def __len__(self) -> int:
            ...
        @property
        def __iter__(self) -> None:
            """
            Cannot be iterated. Use direct access instead.
            """
    DIMENSIONS: typing.ClassVar[int] = 3
    INPUTS: typing.ClassVar[int] = 8
    OUTPUTS: typing.ClassVar[int] = 3
    OUTPUTS_LIST: typing.ClassVar[list]  # value = [<Output.Weight: 0>, <Output.LEO: 1>, <Output.Bias: 2>]
    _docstrings: typing.ClassVar[dict] = {'DIMENSIONS': 'for the I/O coordinates', 'INPUTS': 'Number of inputs', 'OUTPUTS': 'Number of outputs', 'OUTPUTS_LIST': 'The list of output types the CPPN can produce'}
    @staticmethod
    def functions() -> dict[str, typing.Callable[[float], float]]:
        """
        Return a copy of the C++ built-in function set
        """
    @staticmethod
    def outputs() -> CPPN.Outputs:
        """
        Return a buffer in which the CPPN can store output data
        """
    @typing.overload
    def __call__(self, src: Point, dst: Point, buffer: CPPN.Outputs) -> None:
        """
        Evaluates on provided coordinates and retrieve all outputs
        """
    @typing.overload
    def __call__(self, src: Point, dst: Point, type: CPPN.Output) -> float:
        """
        Evaluates on provided coordinates for the requested output
        
        .. note: due to an i686 bug this function is unoptimized on said platforms
        """
    @typing.overload
    def __call__(self, src: Point, dst: Point, buffer: CPPN.Outputs, subset: set[CPPN.Output]) -> None:
        """
        Evaluates on provided coordinates for the requested outputs
        """
    def __init__(self, arg0: _cpp.genotype.CPPNData) -> None:
        ...
class Point:
    """
    3D coordinate using fixed point notation with 3 decimals
    """
    def __eq__(self, arg0: Point) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __init__(self, x: float, y: float, z: float) -> None:
        """
        Create a point with the specified coordinates
        
        Args:
          x, y, z (float): x, y, z coordinate
        """
    def __ne__(self, arg0: Point) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def tuple(self) -> tuple[float, float, float]:
        """
        Return a tuple for easy unpacking in python
        """
