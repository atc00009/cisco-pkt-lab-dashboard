import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Cisco Lab Topology & Activity Dashboard",
    page_icon="🔌",
    layout="wide"
)

st.title("🔌 Cisco Networking Labs & Topology Dashboard")
st.caption("Interactive Packet Tracer topology diagrams and lab activity guides.")

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
        st.graphviz_chart("""
            digraph {
                rankdir=LR;
                bgcolor="#0E1117";
                node [style="filled,rounded", fontname="Arial", fontcolor="white", fontsize=22, width=2.2, height=1.2, margin=0.3, penwidth=2];
                edge [fontname="Arial", fontsize=18, fontcolor="white", penwidth=2.5];
                
                PC1 [label="Inside PC\\n(192.168.1.10)", fillcolor="#2E7D32", shape=box];
                R_Inside [label="Inside Router\\n(R1)", fillcolor="#1565C0", shape=circle];
                R_ISP [label="ISP Router", fillcolor="#EF6C00", shape=circle];
                Server_Ext [label="Web Server\\n(203.0.113.50)", fillcolor="#AD1457", shape=box];
                
                PC1 -> R_Inside [label=" Gi0/0", color="#90CAF9"];
                R_Inside -> R_ISP [label=" Se0/0/0 (NAT)", color="#FFEE58"];
                R_ISP -> Server_Ext [label=" Gi0/1", color="#90CAF9"];
            }
        """, use_container_width=True)
        
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
        st.graphviz_chart("""
            digraph {
                rankdir=LR;
                bgcolor="#0E1117";
                node [style="filled,rounded", fontname="Arial", fontcolor="white", fontsize=22, width=2.2, height=1.2, margin=0.3, penwidth=2];
                edge [fontname="Arial", fontsize=18, fontcolor="white", penwidth=2.5];
                
                Branch_LAN [label="Branch PC\\n(10.10.10.0/24)", fillcolor="#2E7D32", shape=box];
                R_Branch [label="Router Branch", fillcolor="#1565C0", shape=circle];
                Cloud_WAN [label="Internet WAN", fillcolor="#6A1B9A", shape=diamond];
                R_HQ [label="Router HQ", fillcolor="#1565C0", shape=circle];
                HQ_LAN [label="HQ Server\\n(10.20.20.0/24)", fillcolor="#AD1457", shape=box];
                
                Branch_LAN -> R_Branch [label=" LAN", color="#90CAF9"];
                R_Branch -> Cloud_WAN [label=" ISP", color="#90CAF9"];
                Cloud_WAN -> R_HQ [label=" ISP", color="#90CAF9"];
                R_HQ -> HQ_LAN [label=" LAN", color="#90CAF9"];
                R_Branch -> R_HQ [label=" GRE Tunnel 0", color="#69F0AE", constraint=false];
            }
        """, use_container_width=True)
        
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
        st.graphviz_chart("""
            digraph {
                rankdir=LR;
                bgcolor="#0E1117";
                node [style="filled,rounded", fontname="Arial", fontcolor="white", fontsize=22, width=2.2, height=1.2, margin=0.3, penwidth=2];
                edge [fontname="Arial", fontsize=18, fontcolor="white", penwidth=2.5];
                
                R1_PAP [label="Router R1\\n(PAP Client)", fillcolor="#1565C0", shape=circle];
                R2_Central [label="Central ISP Router", fillcolor="#EF6C00", shape=circle];
                R3_CHAP [label="Router R3\\n(CHAP Peer)", fillcolor="#1565C0", shape=circle];
                
                R1_PAP -> R2_Central [label=" PPP Link (PAP)", color="#FF7043"];
                R3_CHAP -> R2_Central [label=" PPP Link (CHAP)", color="#5C6BC0"];
            }
        """, use_container_width=True)
        
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
        st.graphviz_chart("""
            digraph {
                rankdir=LR;
                bgcolor="#0E1117";
                node [style="filled,rounded", fontname="Arial", fontcolor="white", fontsize=22, width=2.2, height=1.2, margin=0.3, penwidth=2];
                edge [fontname="Arial", fontsize=18, fontcolor="white", penwidth=2.5];
                
                SiteA [label="Site A LAN\\n(192.168.10.0/24)", fillcolor="#2E7D32", shape=box];
                GW_A [label="IPSec Gateway A", fillcolor="#1565C0", shape=circle];
                Untrusted [label="Public Internet", fillcolor="#C62828", shape=diamond];
                GW_B [label="IPSec Gateway B", fillcolor="#1565C0", shape=circle];
                SiteB [label="Site B LAN\\n(192.168.20.0/24)", fillcolor="#2E7D32", shape=box];
                
                SiteA -> GW_A [label=" LAN", color="#90CAF9"];
                GW_A -> Untrusted [label=" WAN", color="#90CAF9"];
                Untrusted -> GW_B [label=" WAN", color="#90CAF9"];
                GW_B -> SiteB [label=" LAN", color="#90CAF9"];
                GW_A -> GW_B [label=" IPSec Tunnel", color="#69F0AE", constraint=false];
            }
        """, use_container_width=True)
        
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
