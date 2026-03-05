from pyvis.network import Network
import tempfile
import os

def build_graph(relations):
    """
    Builds an interactive physics-based network graph using PyVis.
    Returns the path to the temporary HTML file containing the graph.
    """
    # Create the network (dark theme physics graph)
    net = Network(height="450px", width="100%", bgcolor="#0f172a", font_color="#f8fafc")
    net.force_atlas_2based()

    # Add nodes and edges safely
    added_nodes = set()
    for r in relations:
        src = str(r.get("source", "Unknown"))
        tgt = str(r.get("target", "Unknown"))
        rel_type = str(r.get("type", "related_to"))
        
        if src not in added_nodes:
            net.add_node(src, label=src, color="#6366f1", size=15)
            added_nodes.add(src)
        if tgt not in added_nodes:
            net.add_node(tgt, label=tgt, color="#a855f7", size=15)
            added_nodes.add(tgt)
            
        net.add_edge(src, tgt, title=rel_type, color="#334155")
        
    # Generate HTML string
    # We use a temporary file to hold the HTML since Streamlit components use raw HTML
    try:
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        net.save_graph(tmp_file.name)
        with open(tmp_file.name, 'r', encoding='utf-8') as f:
            html_data = f.read()
            
        # Cleanup
        tmp_file.close()
        os.unlink(tmp_file.name)
        
        return html_data
    except Exception as e:
        print(f"Error building pyvis graph: {e}")
        return "<p style='color:white;'>Failed to render interactive graph.</p>"