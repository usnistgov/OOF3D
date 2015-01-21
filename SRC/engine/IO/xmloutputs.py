# -*- python -*-
# $RCSfile: xmloutputs.py,v $
# $Revision: 1.2.4.3 $
# $Author: fyc $
# $Date: 2014/07/28 22:18:10 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common.IO import xmlmenudump
from ooflib.engine.IO import output

def _catalogPaths(outputlist, xmlids, prefix):
    for o in outputlist:
        if o not in xmlids:
            xmlids[o] = prefix + o.getPath().replace(':', '-')

def outputDump(file):
    ## TODO 3.1: The output trees have changes, so this needs to be updated.
    scalars = output.scalarOutputs.getObjects()
    positions = output.positionOutputs.getObjects()
    aggregates = output.aggregateOutputs.getObjects()
    allOutputs = scalars + positions + aggregates
    # # allOutputs contains duplicates...
    # allOutputs.sort(lambda x, y: cmp(x.getPath(), y.getPath()))
    xmlids = {}
    _catalogPaths(scalars, xmlids, 'Output-Scalar-')
    _catalogPaths(positions, xmlids, 'Output-Position-')
    _catalogPaths(aggregates, xmlids, 'Output-Aggregates-')

    print >> file, "<section id='Section-Output'>"
    print >> file, " <title>Outputs</title>"
    print >> file, "<!--this section produced by SRC/engine/IO/xmloutputs.py-->"
    print >> file, """
    <para>
     The <classname>Output</classname> classes provide ways of
     extracting data from <link
     linkend='Section-Concepts-Mesh'>Meshes</link>.  Different kinds
     of <classname>Outputs</classname> produce different kinds of
     data.  <link
     linkend='RegisteredClass-FilledContourDisplay'>Contour
     plots</link>, for example, display the results of a <link
     linkend='Section-Output-Scalar'>Scalar Output</link> at
     locations determined by a <link
     linkend='Section-Output-Position'>Position Output</link>.
    </para>
    <para>
      <classname>Outputs</classname> are used for graphical output by
      some <xref linkend="RegisteredClass-DisplayMethod"/> classes,
      for post-processing on the <link
      linkend="Section-Tasks-Analysis">Analysis</link> and <link
      linkend="Section-Tasks-BdyAnalysis">Boundary Analysis</link> pages,
      and as data for
      <link linkend="MenuItem-OOF.Mesh.Scheduled_Output">scheduled
      outputs</link>.
    </para>
    <para>
     The three categories of outputs are
     <itemizedlist>
      <listitem><para id='Section-Output-Scalar'>
       <classname>ScalarOutputs</classname>:
       These are Outputs whose result is a single number at each evaluation
       point.  They are used as the <varname>what</varname> argument
       in the contour plotting commands, for example.
       <itemizedlist spacing='compact'>
       """
    paths = [(o.getPath(),o) for o in scalars]
    paths.sort()
    for path,o in paths:
        xmlmenudump.xmlIndexEntry(path, "Scalar Output", xmlids[o])
        print >> file, " <listitem><simpara><link linkend='%s'>" % xmlids[o]
        print >> file, "  <classname>%s</classname>" % path
        print >> file, " </link></simpara></listitem>"
    print >> file, """
       </itemizedlist>
      </para></listitem>
      <listitem><para id='Section-Output-Position'>
       <classname>PositionOutputs</classname>:
       These are Outputs whose result is a position.  They are used as the
       <varname>where</varname> argument in plotting commands.
        <itemizedlist spacing='compact'>"""
    paths = [(o.getPath(),o) for o in positions]
    paths.sort()
    for path,o in paths:
        xmlmenudump.xmlIndexEntry(path, "Position Output", xmlids[o])
        print >> file, " <listitem><simpara><link linkend='%s'>" % xmlids[o]
        print >> file, "  <classname>%s</classname>" % path
        print >> file, " </link></simpara></listitem>"
    print >> file, """
       </itemizedlist>
      </para></listitem>
      <listitem><para id='Section-Output-Aggregate'>
       <classname>AggregateOutputs</classname>:

       These are Outputs whose result is a (possibly) multidimensional
       object, such as a &field; or &flux;.
       They are used when interactively querying &mesh; data with the
       <link
       linkend='Section-Graphics-MeshInfo-DataViewer'>Data
       Viewer</link>.  Many of the <link
       linkend='Section-Output-Scalar'><classname>ScalarOutputs</classname></link>
       are also <classname>AggregateOutputs</classname>.
       <itemizedlist spacing='compact'> """
    paths = [(o.getPath(),o) for o in aggregates]
    paths.sort()
    for path,o in paths:
        xmlmenudump.xmlIndexEntry(path, "Aggregate Output", xmlids[o])
        print >> file, "<listitem><simpara><link linkend='%s'>" % xmlids[o]
        print >> file, " <classname>%s</classname>" % path
        print >> file, " </link></simpara></listitem>"
    print >> file, """
       </itemizedlist>

      </para></listitem>
     </itemizedlist>
     
    </para>
    """

    # for i in range(len(allOutputs)):
    #     if i==0 or (allOutputs[i] is not allOutputs[i-1]):
    #         o = allOutputs[i]
    for o,xmlid in xmlids.items():
            path = o.getPath()
            # xmlid = xmlids[path]
            print >> file, "<refentry id='%s' role='Output'>" % xmlid
            print >> file, " <refnamediv>"
            print >> file, "  <refname>%s</refname>" % path
            try:
                print >> file, " <refpurpose>%s</refpurpose>" % xmlmenudump.getHelp(o)
            except AttributeError:
                print >> file, " <refpurpose>MISSING TIP STRING: %s</refpurpose>" % xmlid
            print >> file, " </refnamediv>"
            print >> file, " <refsynopsisdiv>"
            print >> file, "  <title>Output Categories</title>"
            print >> file, "  <itemizedlist spacing='compact'>"
            if o in scalars:
                print >> file, "<listitem><simpara><link linkend='Section-Output-Scalar'><classname>ScalarOutput</classname></link></simpara></listitem>"
            if o in positions:
                print >> file, "<listitem><simpara><link linkend='Section-Output-Position'><classname>PositionOutput</classname></link></simpara></listitem>"
            if o in aggregates:
                print >> file, "<listitem><simpara><link linkend='Section-Output-Aggregate'><classname>AggregateOutput</classname></link></simpara></listitem>"
            print >> file, "  </itemizedlist>"
            print >> file, " </refsynopsisdiv>"
            params = o.getSettableParams().values()
            if params:
                print >> file, " <refsect1>"
                print >> file, "  <title>Parameters</title>"
                print >> file, "  <variablelist>"
                for param in params:
                    xmlmenudump.process_param(param)
                    print >> file, "   <varlistentry>"
                    print >> file, "    <term><varname>%s</varname></term>" \
                          % param.name
                    print >> file, "    <listitem>"
                    try:
                        tip = xmlmenudump.getHelp(param)
                    except AttributeError:
                        tip = "MISSING TIP STRING: %s" % param.name
                    print >> file, "     <simpara>%s <emphasis>Type</emphasis>: %s</simpara>" \
                          % (tip, param.valueDesc())
                    print >> file, "     </listitem>"
                    print >> file, "   </varlistentry>"
                print >> file, "  </variablelist>"
                print >> file, " </refsect1>"
            print >> file, " <refsect1>"
            print >> file, "  <title>Description</title>"
            try:
                print >> file, xmlmenudump.getDiscussion(o)
            except AttributeError:
                print >> file, \
                      "<simpara>MISSING DISCUSSION: Output %s</simpara>" % path
            print >> file, " </refsect1>"
            
            print >> file, "</refentry>"
            
    print >> file, "</section>"         # End of Outputs 

xmlmenudump.addSection(outputDump, 2)
