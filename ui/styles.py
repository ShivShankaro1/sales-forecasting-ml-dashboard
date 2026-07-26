import streamlit as st


def load_css() -> None:
    st.markdown(
        """
        <style>
        /* =======================================================
           PREMIUM BRIGHT METALLIC THEME
        ======================================================= */

        :root {
            --bg-primary: #050816;
            --bg-secondary: #0b1020;
            --glass: rgba(15, 23, 42, 0.72);
            --glass-strong: rgba(15, 23, 42, 0.90);
            --cyan: #00e5ff;
            --blue: #38bdf8;
            --purple: #8b5cf6;
            --pink: #ec4899;
            --green: #22c55e;
            --gold: #facc15;
            --text: #f8fafc;
            --muted: #94a3b8;
        }

        /* =======================================================
           APP BACKGROUND WITH ANIMATION
        ======================================================= */

        .stApp {
            background:
                radial-gradient(circle at 8% 8%, rgba(0, 229, 255, 0.26), transparent 28%),
                radial-gradient(circle at 92% 12%, rgba(236, 72, 153, 0.20), transparent 28%),
                radial-gradient(circle at 45% 90%, rgba(139, 92, 246, 0.22), transparent 32%),
                linear-gradient(135deg, #020617 0%, #07111f 35%, #0f172a 70%, #111827 100%);
            color: var(--text);
            animation: appGlow 14s ease-in-out infinite alternate;
        }

        @keyframes appGlow {
            0% {
                background-position: 0% 0%;
            }
            100% {
                background-position: 100% 100%;
            }
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            background-image:
                linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
            background-size: 42px 42px;
            mask-image: linear-gradient(to bottom, rgba(0,0,0,0.75), transparent);
        }

        .stApp::after {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            background:
                linear-gradient(115deg, transparent 0%, rgba(255,255,255,0.04) 42%, transparent 58%);
            animation: metallicSweep 9s ease-in-out infinite;
        }

        @keyframes metallicSweep {
            0% {
                transform: translateX(-80%);
                opacity: 0;
            }
            40% {
                opacity: 0.65;
            }
            100% {
                transform: translateX(80%);
                opacity: 0;
            }
        }

        header[data-testid="stHeader"] {
            background: rgba(2, 6, 23, 0.35);
            backdrop-filter: blur(20px);
        }

        .block-container {
            position: relative;
            z-index: 1;
            padding-top: 2rem;
            padding-left: 4rem;
            padding-right: 4rem;
            max-width: 1600px;
            animation: pageFadeIn 0.55s ease-out;
        }

        @keyframes pageFadeIn {
            0% {
                opacity: 0;
                transform: translateY(16px) scale(0.992);
                filter: blur(4px);
            }
            100% {
                opacity: 1;
                transform: translateY(0) scale(1);
                filter: blur(0);
            }
        }

        /* =======================================================
           SIDEBAR
        ======================================================= */

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(2, 6, 23, 0.98), rgba(8, 13, 28, 0.97)),
                radial-gradient(circle at top, rgba(0, 229, 255, 0.18), transparent 45%);
            border-right: 1px solid rgba(0, 229, 255, 0.25);
            box-shadow:
                18px 0 70px rgba(0, 0, 0, 0.45),
                inset -1px 0 0 rgba(255, 255, 255, 0.05);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 2rem;
        }

        section[data-testid="stSidebar"] h1 {
            font-size: 27px !important;
            font-weight: 950 !important;
            letter-spacing: -0.7px;
            background: linear-gradient(90deg, #ffffff, #67e8f9, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 22px rgba(0, 229, 255, 0.16);
        }

        section[data-testid="stSidebar"] .stCaption {
            color: #a8b3c7 !important;
        }

        div[role="radiogroup"] label {
            padding: 7px 10px !important;
            border-radius: 14px !important;
            margin-bottom: 6px !important;
            transition: all 0.25s ease;
            border: 1px solid transparent;
        }

        div[role="radiogroup"] label:hover {
            background: rgba(0, 229, 255, 0.10);
            border: 1px solid rgba(0, 229, 255, 0.20);
            transform: translateX(3px);
        }

        div[role="radiogroup"] label:has(input:checked) {
            background:
                linear-gradient(135deg, rgba(0,229,255,0.18), rgba(139,92,246,0.18)) !important;
            border: 1px solid rgba(0,229,255,0.35) !important;
            box-shadow: 0 10px 28px rgba(0,229,255,0.12);
        }

        /* =======================================================
           HERO CARD
        ======================================================= */

        .hero {
            position: relative;
            overflow: hidden;
            padding: 46px 50px;
            border-radius: 34px;
            background:
                radial-gradient(circle at 80% 15%, rgba(0, 229, 255, 0.22), transparent 25%),
                radial-gradient(circle at 30% 0%, rgba(236, 72, 153, 0.14), transparent 30%),
                linear-gradient(135deg, rgba(8, 47, 73, 0.82), rgba(30, 41, 95, 0.82), rgba(76, 29, 149, 0.58));
            border: 1px solid rgba(125, 211, 252, 0.42);
            box-shadow:
                0 30px 100px rgba(0, 0, 0, 0.48),
                0 0 55px rgba(0, 229, 255, 0.10),
                inset 0 1px 0 rgba(255, 255, 255, 0.20),
                inset 0 -1px 0 rgba(255, 255, 255, 0.05);
            margin-bottom: 30px;
            animation: heroEnter 0.7s ease-out;
        }

        @keyframes heroEnter {
            0% {
                opacity: 0;
                transform: translateY(22px) scale(0.985);
            }
            100% {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        .hero::before {
            content: "";
            position: absolute;
            width: 520px;
            height: 520px;
            right: -130px;
            top: -180px;
            background:
                radial-gradient(circle, rgba(0, 229, 255, 0.42), rgba(168, 85, 247, 0.18), transparent 66%);
            filter: blur(10px);
            opacity: 0.9;
            animation: orbFloat 7s ease-in-out infinite alternate;
        }

        @keyframes orbFloat {
            0% {
                transform: translateY(0) translateX(0);
            }
            100% {
                transform: translateY(30px) translateX(-25px);
            }
        }

        .hero::after {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(120deg, transparent 0%, rgba(255, 255, 255, 0.10) 38%, transparent 60%);
            transform: translateX(-60%);
            animation: heroSweep 6s ease-in-out infinite;
            pointer-events: none;
        }

        @keyframes heroSweep {
            0% {
                transform: translateX(-65%);
            }
            100% {
                transform: translateX(110%);
            }
        }

        .hero h1 {
            position: relative;
            margin: 0;
            font-size: 52px;
            line-height: 1.08;
            font-weight: 950;
            letter-spacing: -1.8px;
            color: #ffffff;
            text-shadow:
                0 10px 45px rgba(0, 0, 0, 0.40),
                0 0 20px rgba(0, 229, 255, 0.14);
            max-width: 1180px;
        }

        .hero p {
            position: relative;
            margin-top: 20px;
            color: #e0f2fe;
            font-size: 18px;
            line-height: 1.8;
            max-width: 1120px;
        }

        .pill-row {
            position: relative;
            margin-top: 26px;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }

        .pill {
            padding: 10px 17px;
            border-radius: 999px;
            background:
                linear-gradient(135deg, rgba(15, 23, 42, 0.94), rgba(30, 41, 59, 0.80));
            border: 1px solid rgba(125, 211, 252, 0.34);
            color: #ecfeff;
            font-size: 13px;
            font-weight: 900;
            box-shadow:
                0 12px 26px rgba(0, 0, 0, 0.28),
                inset 0 1px 0 rgba(255, 255, 255, 0.12);
            transition: all 0.25s ease;
        }

        .pill:hover {
            transform: translateY(-3px);
            border-color: rgba(0, 229, 255, 0.72);
            box-shadow: 0 16px 34px rgba(0, 229, 255, 0.12);
        }

        /* =======================================================
           KPI CARDS
        ======================================================= */

        .kpi-card {
            position: relative;
            overflow: hidden;
            min-height: 154px;
            padding: 25px;
            border-radius: 26px;
            background:
                radial-gradient(circle at top right, rgba(0, 229, 255, 0.16), transparent 38%),
                linear-gradient(145deg, rgba(15, 23, 42, 0.96), rgba(17, 24, 39, 0.88));
            border: 1px solid rgba(148, 163, 184, 0.24);
            box-shadow:
                0 24px 60px rgba(0, 0, 0, 0.36),
                inset 0 1px 0 rgba(255, 255, 255, 0.11);
            transition: all 0.28s ease;
            animation: cardRise 0.55s ease-out;
        }

        @keyframes cardRise {
            0% {
                opacity: 0;
                transform: translateY(15px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .kpi-card:hover {
            transform: translateY(-6px);
            border-color: rgba(0, 229, 255, 0.55);
            box-shadow:
                0 30px 78px rgba(0, 0, 0, 0.48),
                0 0 35px rgba(0, 229, 255, 0.14),
                inset 0 1px 0 rgba(255, 255, 255, 0.16);
        }

        .kpi-card::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, #00e5ff, #818cf8, #d946ef, #22c55e);
        }

        .kpi-card::after {
            content: "";
            position: absolute;
            right: -40px;
            bottom: -40px;
            width: 120px;
            height: 120px;
            background: radial-gradient(circle, rgba(0,229,255,0.12), transparent 70%);
        }

        .kpi-label {
            color: #93c5fd;
            font-size: 12px;
            font-weight: 950;
            text-transform: uppercase;
            letter-spacing: 0.14em;
        }

        .kpi-value {
            margin-top: 14px;
            color: #ffffff;
            font-size: 35px;
            font-weight: 950;
            line-height: 1.05;
            word-break: break-word;
            text-shadow: 0 8px 28px rgba(0, 0, 0, 0.42);
        }

        .kpi-note {
            margin-top: 13px;
            color: #22d3ee;
            font-size: 13px;
            font-weight: 900;
        }

        /* =======================================================
           GLASS BOXES
        ======================================================= */

        .info-box,
        .success-box,
        .warning-box,
        .error-box {
            padding: 18px 20px;
            border-radius: 18px;
            margin: 15px 0;
            backdrop-filter: blur(14px);
            box-shadow:
                0 16px 42px rgba(0, 0, 0, 0.26),
                inset 0 1px 0 rgba(255, 255, 255, 0.08);
            animation: pageFadeIn 0.55s ease-out;
        }

        .info-box {
            background: linear-gradient(135deg, rgba(8, 47, 73, 0.72), rgba(15, 23, 42, 0.72));
            border: 1px solid rgba(56, 189, 248, 0.34);
            border-left: 5px solid #00e5ff;
            color: #dbeafe;
        }

        .success-box {
            background: linear-gradient(135deg, rgba(20, 83, 45, 0.58), rgba(15, 23, 42, 0.72));
            border: 1px solid rgba(34, 197, 94, 0.34);
            border-left: 5px solid #22c55e;
            color: #bbf7d0;
        }

        .warning-box {
            background: linear-gradient(135deg, rgba(120, 53, 15, 0.58), rgba(15, 23, 42, 0.72));
            border: 1px solid rgba(245, 158, 11, 0.34);
            border-left: 5px solid #f59e0b;
            color: #fde68a;
        }

        .error-box {
            background: linear-gradient(135deg, rgba(127, 29, 29, 0.58), rgba(15, 23, 42, 0.72));
            border: 1px solid rgba(239, 68, 68, 0.34);
            border-left: 5px solid #ef4444;
            color: #fecaca;
        }

        /* =======================================================
           TABLES / DATAFRAME
        ======================================================= */

        div[data-testid="stDataFrame"] {
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.20);
            box-shadow:
                0 20px 50px rgba(0, 0, 0, 0.24),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
        }

        /* =======================================================
           TABS
        ======================================================= */

        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            border-bottom: 1px solid rgba(148, 163, 184, 0.20);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 999px;
            padding: 10px 19px;
            background: rgba(15, 23, 42, 0.88);
            border: 1px solid rgba(148, 163, 184, 0.20);
            color: #cbd5e1;
            font-weight: 900;
            transition: all 0.25s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            border-color: rgba(0, 229, 255, 0.50);
            transform: translateY(-2px);
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #0ea5e9, #7c3aed, #ec4899) !important;
            color: white !important;
            border-color: rgba(125, 211, 252, 0.56) !important;
            box-shadow: 0 12px 30px rgba(139, 92, 246, 0.25);
        }

        /* =======================================================
           BUTTONS
        ======================================================= */

        .stButton > button {
            border-radius: 17px;
            border: 1px solid rgba(125, 211, 252, 0.44);
            background:
                linear-gradient(135deg, #0284c7 0%, #4f46e5 48%, #9333ea 100%);
            color: white;
            font-weight: 950;
            padding: 0.76rem 1.2rem;
            box-shadow:
                0 16px 40px rgba(79, 70, 229, 0.30),
                inset 0 1px 0 rgba(255, 255, 255, 0.20);
            transition: all 0.24s ease;
        }

        .stButton > button:hover {
            transform: translateY(-3px) scale(1.01);
            border-color: rgba(0, 229, 255, 0.85);
            box-shadow:
                0 22px 52px rgba(79, 70, 229, 0.46),
                0 0 28px rgba(0, 229, 255, 0.20);
        }

        .stDownloadButton > button {
            border-radius: 17px;
            border: 1px solid rgba(34, 197, 94, 0.50);
            background:
                linear-gradient(135deg, #059669 0%, #16a34a 45%, #22c55e 100%);
            color: white;
            font-weight: 950;
            padding: 0.76rem 1.2rem;
            box-shadow:
                0 16px 40px rgba(34, 197, 94, 0.24),
                inset 0 1px 0 rgba(255, 255, 255, 0.18);
        }

        .stDownloadButton > button:hover {
            transform: translateY(-3px);
            box-shadow:
                0 22px 52px rgba(34, 197, 94, 0.38),
                0 0 28px rgba(34, 197, 94, 0.18);
        }

        /* =======================================================
           INPUTS / UPLOADER
        ======================================================= */

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        textarea,
        input {
            border-radius: 15px !important;
        }

        section[data-testid="stFileUploaderDropzone"] {
            border-radius: 26px;
            background:
                radial-gradient(circle at top right, rgba(0, 229, 255, 0.12), transparent 34%),
                linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(30, 41, 59, 0.70));
            border: 1px dashed rgba(0, 229, 255, 0.45);
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.10),
                0 16px 40px rgba(0,0,0,0.22);
        }

        /* =======================================================
           HEADINGS / SCROLLBAR
        ======================================================= */

        h1, h2, h3 {
            letter-spacing: -0.7px;
        }

        h2, h3 {
            color: #f8fafc;
            text-shadow: 0 10px 34px rgba(0,0,0,0.28);
        }

        ::-webkit-scrollbar {
            width: 12px;
            height: 12px;
        }

        ::-webkit-scrollbar-track {
            background: #020617;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #00e5ff, #7c3aed, #ec4899);
            border-radius: 999px;
            border: 3px solid #020617;
        }

        .stDeployButton {
            opacity: 0.82;
        }

        /* =======================================================
           OPTIONAL VIDEO BACKGROUND SUPPORT
        ======================================================= */

        .video-bg {
            position: fixed;
            inset: 0;
            z-index: -2;
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.18;
            filter: saturate(1.25) contrast(1.1) brightness(0.75);
        }

        .video-overlay {
            position: fixed;
            inset: 0;
            z-index: -1;
            background:
                radial-gradient(circle at 15% 15%, rgba(0,229,255,0.18), transparent 30%),
                linear-gradient(135deg, rgba(2,6,23,0.88), rgba(15,23,42,0.78));
            pointer-events: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )