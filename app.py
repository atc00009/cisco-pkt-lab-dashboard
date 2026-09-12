import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import pandas as pd

st.set_page_config(
    page_title="Cisco Lab Topology & Activity Dashboard",
    page_icon="🔌",
    layout="wide"
)

st.title("🔌 Cisco Networking Labs & Topology Dashboard")
st.caption("Interactive Packet Tracer topology diagrams and lab activity guides.")

def render_packet_tracer_graph(nodes, edges, tab_key):
    """Generates a dark-themed, perfectly centered network topology graph."""
    net = Network(height="450px", width="100%", bgcolor="#0E1117", font_color="white")
    
    # Configure physics to pull nodes into the center and freeze them once settled
    net.set_options("""
    var options = {
      "nodes": {
        "font": { "size": 14, "color": "#FFFFFF" }
      },
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.03,
          "springLength": 100,
          "springConstant": 0.08
        },
        "maxVelocity": 50,
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": { "enabled": true, "iterations": 150 }
      }
    }
    """)
    
    for node in nodes:
        net.add_node(
            node["id"],
            label=node["label"],
            title=f"Device: {node['label']}\nType: {node['type']}\nIP: {node.get('ip', 'N/A')}",
            color=node.get("color", "#0080FF"),
            shape=node.get("shape", "dot"),
            size=25
        )
    for edge in edges:
        net.add_edge(
            edge["from"], 
            edge["to"], 
            title=edge.get("label", ""),
            label=edge.get("label", ""),
            color=edge.get("color", "#848484"),
            width=2
        )
        
    filename = f"topology_{tab_key}.html"
    net.save_graph(filename)
    
    with open(filename, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Force dark background, centered flexbox layout, and visible border on the iframe container
    custom_dark_style = """
    <style>
        html, body {
            background-color: #0E1117 !important;
            margin: 0 !important;
            padding: 0 !important;
            height: 100% !important;
            width: 100% !important;
            overflow: hidden !important;
        }
        #mynetwork {
            background-color: #0E1117 !important;
            border: 1px solid #262730 !important;
            border-radius: 8px !important;
            width: 100% !important;
            height: 440px !important;
        }
    </style>
    """
    html_content = html_content.replace("<head>", f"<head>{custom_dark_style}")
    
    components.html(html_content, height=460)

# -----------------------------------------------------------------------------
# TAB DEFINITIONS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Static & Dynamic NAT", 
    "2. VPN with GRE", 
    "3. PAP & CHAP Config", 
    "4. VPN with IPSec"
])

# =============================================================================
# TAB 1: STATIC AND DYNAMIC NAT
# =============================================================================
with tab1:
    st.header("Workshop 7 / Lab 1: Static and Dynamic NAT")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Network Packet Diagram (Topology)")
        t1_nodes = [
            {"id": "PC1", "label": "Inside PC\n(192.168.1.10)", "type": "Host", "color": "#4CAF50", "shape": "square"},
            {"id": "R_Inside", "label": "Inside Router\n(R1)", "type": "Router", "color": "#0080FF", "shape": "dot"},
            {"id": "R_ISP", "label": "ISP Router", "type": "Router", "color": "#FF9800", "shape": "dot"},
            {"id": "Server_Ext", "label": "Web Server\n(203.0.113.50)", "type": "Server", "color": "#E91E63", "shape": "triangle"}
        ]
        t1_edges = [
            {"from": "PC1", "to": "R_Inside", "label": "Gi0/0 (192.168.1.1)"},
            {"from": "R_Inside", "to": "R_ISP", "label": "Se0/0/0 (NAT Pool)", "color": "#FFC107"},
            {"from": "R_ISP", "to": "Server_Ext", "label": "Gi0/1"}
        ]
        render_packet_tracer_graph(t1_nodes, t1_edges, tab_key="nat")
        
    with col2:
        st.subheader("Lab Specifications")
        st.markdown("**Overview:** Configure Static NAT for server mapping and Dynamic NAT with PAT (Overload) for LAN hosts.")
        
        df_t1 = pd.DataFrame({
            "Device": ["R1", "R1", "ISP"],
            "Interface": ["GigabitEthernet0/0", "Serial0/0/0", "Serial0/0/0"],
            "NAT Role": ["ip nat inside", "ip nat outside", "N/A"],
            "IP Address": ["192.168.1.1/24", "203.0.113.1/30", "203.0.113.2/30"]
        })
        st.dataframe(df_t1, use_container_width=True)
        
        with st.expander("Show Configuration Commands"):
            st.code("""
# Static NAT Setup
ip nat inside source static 192.168.1.10 203.0.113.10

# Dynamic NAT with Overload (PAT) Setup
access-list 1 permit 192.168.1.0 0.0.0.255
ip nat pool MY_POOL 203.0.113.1 203.0.113.5 netmask 255.255.255.248
ip nat inside source list 1 pool MY_POOL overload

# Interface Assignment
interface g0/0
 ip nat inside
interface s0/0/0
 ip nat outside
            """, language="bash")

# =============================================================================
# TAB 2: VPN WITH GRE
# =============================================================================
with tab2:
    st.header("Workshop 7 / Lab 2: Configuring VPN with GRE")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Network Packet Diagram (Topology)")
        t2_nodes = [
            {"id": "Branch_LAN", "label": "Branch PC\n(10.10.10.0/24)", "type": "Host", "color": "#4CAF50", "shape": "square"},
            {"id": "R_Branch", "label": "Router Branch", "type": "Router", "color": "#0080FF", "shape": "dot"},
            {"id": "Cloud_WAN", "label": "Internet WAN", "type": "Cloud", "color": "#9C27B0", "shape": "diamond"},
            {"id": "R_HQ", "label": "Router HQ", "type": "Router", "color": "#0080FF", "shape": "dot"},
            {"id": "HQ_LAN", "label": "HQ Server\n(10.20.20.0/24)", "type": "Server", "color": "#E91E63", "shape": "triangle"}
        ]
        t2_edges = [
            {"from": "Branch_LAN", "to": "R_Branch", "label": "LAN Access"},
            {"from": "R_Branch", "to": "Cloud_WAN", "label": "Physical ISP (172.16.1.1)"},
            {"from": "Cloud_WAN", "to": "R_HQ", "label": "Physical ISP (172.16.2.1)"},
            {"from": "R_HQ", "to": "HQ_LAN", "label": "LAN Access"},
            {"from": "R_Branch", "to": "R_HQ", "label": "GRE Tunnel 0", "color": "#00E676"}
        ]
        render_packet_tracer_graph(t2_nodes, t2_edges, tab_key="gre")
        
    with col2:
        st.subheader("Lab Specifications")
        st.markdown("**Overview:** Establish a Generic Routing Encapsulation (GRE) point-to-point tunnel to pass unencrypted corporate traffic across an untrusted WAN.")
        
        df_t2 = pd.DataFrame({
            "Router": ["R_Branch", "R_HQ"],
            "Tunnel ID": ["Tunnel 0", "Tunnel 0"],
            "Tunnel IP": ["192.168.100.1/30", "192.168.100.2/30"],
            "Physical Src/Dst": ["172.16.1.1 -> 172.16.2.1", "172.16.2.1 -> 172.16.1.1"]
        })
        st.dataframe(df_t2, use_container_width=True)
        
        with st.expander("Show Configuration Commands"):
            st.code("""
# R_Branch GRE Tunnel Config
interface Tunnel0
 ip address 192.168.100.1 255.255.255.252
 tunnel source Serial0/0/0
 tunnel destination 172.16.2.1
 ip route 10.20.20.0 255.255.255.0 Tunnel0
            """, language="bash")

# =============================================================================
# TAB 3: PAP & CHAP AUTHENTICATION
# =============================================================================
with tab3:
    st.header("Workshop 7 / Lab 3a: EXTENSION Configuring PAP & CHAP")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Network Packet Diagram (Topology)")
        t3_nodes = [
            {"id": "R1_PAP", "label": "Router R1\n(PAP Client)", "type": "Router", "color": "#0080FF", "shape": "dot"},
            {"id": "R2_Central", "label": "Central ISP Router", "type": "Router", "color": "#FF9800", "shape": "dot"},
            {"id": "R3_CHAP", "label": "Router R3\n(CHAP Peer)", "type": "Router", "color": "#0080FF", "shape": "dot"}
        ]
        t3_edges = [
            {"from": "R1_PAP", "to": "R2_Central", "label": "PPP Link (PAP)", "color": "#FF5722"},
            {"from": "R3_CHAP", "to": "R2_Central", "label": "PPP Link (CHAP)", "color": "#3F51B5"}
        ]
        render_packet_tracer_graph(t3_nodes, t3_edges, tab_key="ppp")
        
    with col2:
        st.subheader("Lab Specifications")
        st.markdown("**Overview:** Configure Point-to-Point Protocol (PPP) serial encapsulation with plain-text Password Authentication Protocol (PAP) and challenge-response CHAP security.")
        
        df_t3 = pd.DataFrame({
            "Link": ["R1 <-> R2", "R3 <-> R2"],
            "Encapsulation": ["PPP", "PPP"],
            "Auth Protocol": ["PAP (Cleartext)", "CHAP (MD5 Hash)"],
            "Handshake": ["2-Way", "3-Way"]
        })
        st.dataframe(df_t3, use_container_width=True)
        
        with st.expander("Show Configuration Commands"):
            st.code("""
# R1 PAP Setup
username R2 secret CiscoPAP123
interface Serial0/0/0
 encapsulation ppp
 ppp authentication pap
 ppp pap sent-username R1 password CiscoPAP123

# R3 CHAP Setup
username R2 secret CiscoCHAP123
interface Serial0/0/1
 encapsulation ppp
 ppp authentication chap
            """, language="bash")

# =============================================================================
# TAB 4: VPN WITH IPSEC
# =============================================================================
with tab4:
    st.header("Workshop 7 / Lab 3b: EXTENSION Configuring VPN with IPSec")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Network Packet Diagram (Topology)")
        t4_nodes = [
            {"id": "SiteA", "label": "Site A LAN\n(192.168.10.0/24)", "type": "Host", "color": "#4CAF50", "shape": "square"},
            {"id": "GW_A", "label": "IPSec Gateway A", "type": "Router", "color": "#0080FF", "shape": "dot"},
            {"id": "Untrusted", "label": "Public Internet", "type": "Cloud", "color": "#F44336", "shape": "diamond"},
            {"id": "GW_B", "label": "IPSec Gateway B", "type": "Router", "color": "#0080FF", "shape": "dot"},
            {"id": "SiteB", "label": "Site B LAN\n(192.168.20.0/24)", "type": "Host", "color": "#4CAF50", "shape": "square"}
        ]
        t4_edges = [
            {"from": "SiteA", "to": "GW_A", "label": "LAN"},
            {"from": "GW_A", "to": "Untrusted", "label": "WAN"},
            {"from": "Untrusted", "to": "GW_B", "label": "WAN"},
            {"from": "GW_B", "to": "SiteB", "label": "LAN"},
            {"from": "GW_A", "to": "GW_B", "label": "IPSec Tunnel", "color": "#00E676"}
        ]
        render_packet_tracer_graph(t4_nodes, t4_edges, tab_key="ipsec")
        
    with col2:
        st.subheader("Lab Specifications")
        st.markdown("**Overview:** Secure site-to-site communication using IKE Phase 1 (ISAKMP) and IKE Phase 2 Crypto Maps.")
        
        df_t4 = pd.DataFrame({
            "Phase": ["IKE Phase 1", "IKE Phase 2"],
            "Parameter": ["ISAKMP Policy", "IPSec Transform Set"],
            "Algorithms": ["AES-256, SHA-256, DH Group 5", "esp-aes esp-sha-hmac"],
            "Authentication": ["Pre-Shared Key (PSK)", "Crypto Map Application"]
        })
        st.dataframe(df_t4, use_container_width=True)
        
        with st.expander("Show Configuration Commands"):
            st.code("""
# IKE Phase 1
crypto isakmp policy 10
 encr aes 256
 hash sha256
 authentication pre-share
 group 5
crypto isakmp key VPN_Secret_Key address 209.165.201.1

# IKE Phase 2
crypto ipsec transform-set MY_SET esp-aes esp-sha-hmac
crypto map MY_MAP 10 ipsec-isakmp
 set peer 209.165.201.1
 set transform-set MY_SET
 match address 101

# Apply to Interface
interface s0/0/0
 crypto map MY_MAP
            """, language="bash")
