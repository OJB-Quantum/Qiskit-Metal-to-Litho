# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent
from shapely.geometry import CAP_STYLE, JOIN_STYLE

from ... import config
if not config.is_building_docs():
    from qiskit_metal import is_true


class BigDot(QComponent):
    """A single configurable circle.

    QComponent class.

    .. image::
        CircleRaster.png

    .. meta::
        Circle Raster

    Default Options:
        * radius: '1um'
        * resolution: '16'
        * cap_style: 'round' -- Valid options are 'round', 'flat', 'square'
        * subtract: 'False'
        * helper: 'False'
    """

    # Edit these to define your own template options for creation
    # Default drawing options
    # default_options = Dict()

    default_options = dict(
        radius='0.05um',
        resolution='16',
        cap_style='round',  # round, flat, square
        # join_style = 'round', # round, mitre, bevel
        # General
        subtract='False',
        helper='False')
    """Default drawing options"""

    # Name prefix of component, if user doesn't provide name
    component_metadata = Dict(short_name='compdot')
    """Component metadata"""

    TOOLTIP = """A single configurable circle"""

    def make(self):
        """The make function implements the logic that creates the geoemtry
        (poly, path, etc.) from the qcomponent.options dictionary of
        parameters, and the adds them to the design, using
        qcomponent.add_qgeometry(...), adding in extra needed information, such
        as layer, subtract, etc."""
        
        """Convert self.options into QGeometry."""
        # name = 'Dot'
        p = self.p  # p for parsed parameters. Access to the parsed options.

        # EDIT HERE - Replace the following with your code
        # Create some raw geometry
        # Use autocompletion for the `draw.` module (use tab key)
        
        # API reference items can be found by using the search bar on https://shapely.readthedocs.io/en/stable/geometry.html
        
        # Create the geometry. #Use parameters set by you in the dictionary above (under 'default options')
        circle = draw.Point(p.pos_x, p.pos_y).buffer(
            p.radius,
            resolution=int(p.resolution),
            cap_style=getattr(CAP_STYLE, p.cap_style),
            #join_style = getattr(JOIN_STYLE, p.join_style)
        )
        
        geom5 = {'my_dot': circle}
        self.add_qgeometry('poly', geom5, subtract=p.subtract, helper=p.helper, layer=p.layer, chip=p.chip)
        
        # self.add_qgeometry('poly', geom3, layer=p.layer, subtract=False)
        
        
#OBBOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOooOOOOOOOOOOOOOOOOOB
#BBBOBOOOOoooooooooooooooooooooooooooooooooooooooo:ooooooo:oOOOOOOOOB
#BBBBBBOOO:.................................................oOOOOOOOB
#BBBBBBBBO:oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo.oOOOOOOOB
#BBBBBBBBB:oOBOOOOOOOOOOOOOBOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo.oOOOOOOOB
#BBBBBBBBB:oBBBBBBBBBBBOOOBBOOOOOBBOOOOOOOOOOOOOOOOOOOOOOOo.oOOOOOOOB
#BBBBBBBBB:oBBBBBBBBBBBOOBBOOOOOOBBBBOOOOOOOOOOOOOOOOOOOOOo.OOOOOOOOB
#BBBBBBBBB::BBBBBBBBBBOOBBBOOOOOOBBBBBOOOOOOOOOOOOOOOOOOOOo.OOOOOOOOB
#BBBBBBBBB::BBBBBBBBBBBBBBBOOOOOOBBBBBOOOOOOOOOOOOOOOOOOOOo.OOOOOOOOB
#BBBBBBBBB::BBBBBBBBBBBBBBBOOOOOOBBBBBOOOOOOOOOOOOOOOOOOOOo.OOOOOOOOB
#BBBBBBBBB::BBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo.OOOOOOOOB
#BBBBBBBBB::BBBBBBOBBBBBBBBOOOOOOBBBBBBBBOOOOOOOOOOOOOOOOOo.OOOOOOOOB
#BBBBBBBBBo:BBBBBBBBBBBBBBBBBBBBOBBBBBBBBOOBOOOOOOOOOOOOOOo.OOOBOOOOB
#BBBBBBBBBo:BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOo:OOBBOOOOB
#BBBBBBBBBo:BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOo:OBBBBBBBB
#BBBBBBBBBo:BBBBOOBBOOBOOOBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOo:OBBBBBBBB
#BBBBBBBBBo:OOOO:.oO..Bo.oBBBBBBBBBBBBBBBBBBO:.oO..Oo.:OOOo:BBBBBBBBO
#OOOOOOOOOo:OOoo:.OO..Bo.oBBBBBBBBBBBBBBBBBBB:.OO..Bo.:OOOo:BBBBBBBBO
#OOOOOOOOOo.Oo..:oOBooBOoOBBBBBBBBBBBBBBBBBBBooOBooBO:::OB::BBBBBBBBO
#OOOOOOOOOo.OO::oBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOBBBBO..oO::BBBBBBBBO
#OOOOOOOOOo.OOOOOBBBBBBBBBBBBBBBBBBBBBBBBBOOBBBBBBBBBOo:OB::BBBBBBBBO
#OOOOOOOOOo.OO::oBBBBBBBBBBBBBBBBBBBBBBBBOooOOBBBBBBBBBOBB::BBBBBBBBO
#OOOOOOOOOo.OO..oBBBBBBBBBBBBBBBBBOOBBBBBOooOoOBBBBBBO..OB:oBBBBBBBBO
#OOOOOOOOOo.OOooOBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOBBBBBBO..OB:oBBBBBBBBO
#OOOOOOOOOo.OOoOOBBBBBBBBBBBBBBBBBBBBBBBBOOOBOOBBBBBBBOOBB:oBBBBBBBBO
#OOOOOOOOOO.OO..oBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOBBBBBBOOoBB:oBBBBBBBBO
#OOOOOOOOOO.OO:.:OBOOBBOOBBBBBBBBBBBBBBBBBBBBOOBOOBBOo..OB:oBBBBBBBBO
#OOOOOOOOOO.OOOo.:Bo.OB..BBBBBBBBBBBBBBBBBBB:.oB..BO.:::BB:oBBBBBBBBO
#OOOOOOOOOO.OOOo.:B:.oO..BBBBBBBBBBBBBBBBBBB:.:O..Oo.:BBBB:oBBBBBBBBO
#OOOOOOOOOO.oOOoooBOOBBOOBBBBBBBBBBBBBBBBBBBo:ooo:OOoOBBBB:OBBBBBBBBO
#OOOOOOOOoo.ooooooBBBBBBBBBBBBBBBBBBBBBBBBBOoOOOOooBBBBBBB.OBBBBBBBBO
#OOOOOOOOoo.ooooOOBBBBBBBBBBBBBBBBBBBBBBBBOooOOOOOoOBBBBBB.OBBBBBBBBO
#OOOOOOOooo.ooOOOOBBBBBBBBBBBBBBBBBBBBBBBBooooOOOOooOBBBBO.OBBBBBBBBO
#OOOOOOoooo:ooOOOOBBBBBBBBBBBBBBBBBBBBBBBOoooooOOOoooOOOBB.OBBBBBBBBO
#OOOOOOoooo:ooOOOOBBBBBBBBBBBBBBBBBBBBBBOoooooOOOOOooooooO.OBBBBBBBBB
#BBBOoooooo:oooOBBBBBBBBBBBBBBBBBBBBBBBBoooooOOOOOOooooooo.OBBBBBBBBB
#BBBOoooooo:oooOBBBBBBBBBBBBBBBBBBBBBBBOooooOOOOOooOoooooo.OBBBBBBBBB
#BBBOoooooo:ooooOBBBBBBBBBBBBBBBBBBBBBOoooOOOOOOooOOOOOooo.OBBBBBBBBB
#BBBOOooooo:ooooOBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOoOOOOOOOOo:OOBBBBBBBB
#BBBBOooooO:ooooOBBBBBBBBBBBBBBBBBBBBOOOOOOOBOOOOOOOOOOOOo:OOBBBBBBBB
#BBBBOooooO:oooooOBBBBBBBBBBBBBBBBBBBOOOBBBBBOOOOOOOOOOOOo:OOBBBBBBBB
#BBBBOooooo::::::::::::::::::::oooooo::oooooooooooooooooo::OBBBBBBBBB
#BBBBOOooooo:::::::o::::::::::::::::::::::::::::::::::::..:BBBBBBBBBB
#BBBBOOOOOOOOOOOOooOBBBBBBBBBBBBBBBBBOOBBBBBBBBOOOOOOOOOOOBBBBBBBBBBO
#OBBBOOOOOOOOOOOOOoOBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOBBBBBBBBBBB