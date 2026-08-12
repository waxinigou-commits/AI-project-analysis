import { useEffect, useMemo, useState } from "react";
import type { Product } from "./types";

const COLORS = ["#b7f36b", "#7bdff2", "#f6aeff", "#ffd166", "#9fa8ff"];

function Icon({ children }: { children: string }) {
  return <span className="icon" aria-hidden="true">{children}</span>;
}

function Brand() {
  return <div className="brand"><span className="brand-mark"><i /><i /><i /></span><span>AI SIGNAL</span></div>;
}

function ScoreRing({ score }: { score: number }) {
  return <div className="score-ring" style={{ "--score": `${score * 3.6}deg` } as React.CSSProperties}><span>{score}</span></div>;
}

function Sparkline({ values }: { values: number[] }) {
  const max = Math.max(...values); const min = Math.min(...values);
  const pts = values.map((v, i) => `${(i/(values.length-1))*100},${30-((v-min)/(max-min||1))*24}`).join(" ");
  return <svg className="spark" viewBox="0 0 100 34" preserveAspectRatio="none" aria-label="趋势图"><polyline points={pts} /></svg>;
}

function ProductLogo({ name, index = 0 }: { name: string; index?: number }) {
  return <div className="product-logo" style={{ background: COLORS[index % COLORS.length] }}>{name.slice(0, 1).toUpperCase()}</div>;
}

function Detail({ product, close }: { product: Product; close: () => void }) {
  return <div className="detail-backdrop" onMouseDown={close}>
    <aside className="detail" onMouseDown={e => e.stopPropagation()} aria-label="产品详情">
      <button className="close" onClick={close} aria-label="关闭">×</button>
      <div className="detail-head"><ProductLogo name={product.name}/><div><p className="eyebrow">{product.category} · {product.source}</p><h2>{product.name}</h2><p>{product.tagline}</p></div><ScoreRing score={product.score}/></div>
      <div className="detail-meta"><span>发布于 {product.launchedAt}</span><span>事实：{product.factStatus}</span><span>核验于 {product.verifiedAt}</span></div>
      <div className="analysis-disclaimer"><b>AI 分析</b><span>{product.analysisNote} · 分析置信度 {product.confidence}%</span></div>
      <section><h3>分析 · 一句话定位</h3><p>{product.positioning}</p></section>
      <div className="detail-grid"><section><h3>分析 · 目标用户</h3><div className="tags">{product.targetUsers.map(x => <span key={x}>{x}</span>)}</div></section><section><h3>分析 · 商业模式</h3><p>{product.businessModel}</p></section></div>
      <div className="detail-grid"><section><h3>收费模式</h3><p className="big-copy">{product.pricingModel}</p></section><section><h3>主要竞品</h3><div className="tags neutral">{product.competitors.map(x => <span key={x}>{x}</span>)}</div></section></div>
      <section><h3>分析 · 增长机会</h3><ol className="opportunities">{product.opportunities.map((x,i) => <li key={x}><b>0{i+1}</b><span>{x}</span></li>)}</ol></section>
      <section><h3>分析 · 风险判断</h3><ul className="risks">{product.risks.map(x => <li key={x}>{x}</li>)}</ul></section>
      <a className="source-link" href={product.sourceUrl} target="_blank" rel="noreferrer">查看原始发布页 ↗</a>
    </aside>
  </div>;
}

export default function App() {
  const [products, setProducts] = useState<Product[]>([]);
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("全部");
  const [period, setPeriod] = useState("30 天");
  const [selected, setSelected] = useState<Product | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => { fetch("./data/products.json").then(r => r.json()).then(setProducts).catch(() => setProducts([])); }, []);
  useEffect(() => { const fn = (e: KeyboardEvent) => e.key === "Escape" && setSelected(null); addEventListener("keydown", fn); return () => removeEventListener("keydown", fn); }, []);
  const categories = ["全部", ...Array.from(new Set(products.map(p => p.category)))];
  const filtered = useMemo(() => {
    const days = Number.parseInt(period);
    const latest = products.reduce((max, p) => Math.max(max, Date.parse(p.launchedAt)), 0);
    const threshold = latest - (Number.isFinite(days) ? days : 30) * 86400000;
    return products.filter(p => Date.parse(p.launchedAt) >= threshold && (category === "全部" || p.category === category) && `${p.name} ${p.tagline} ${p.positioning} ${p.targetUsers.join(" ")}`.toLowerCase().includes(query.toLowerCase()));
  }, [products, query, category, period]);
  const avg = Math.round(products.reduce((s,p)=>s+p.score,0)/(products.length||1));
  const latestLaunch = products.reduce((max,p)=>Math.max(max,Date.parse(p.launchedAt)),0);
  const recentCount = products.filter(p=>Date.parse(p.launchedAt)>=latestLaunch-7*86400000).length;
  const catStats = useMemo(() => categories.slice(1).map((c,i) => ({ name:c, count:products.filter(p=>p.category===c).length, color:COLORS[i%COLORS.length] })).sort((a,b)=>b.count-a.count).slice(0,5), [products]);
  const maxCat = Math.max(...catStats.map(x=>x.count),1);
  const lastVerified = products.map(p=>p.verifiedAt).sort().at(-1) || "—";

  return <div className="app-shell">
    <header><Brand/><nav><a className="active" href="#products">产品雷达</a><a href="#trends">趋势洞察</a><a href="#agent">Codex Agent</a><a href="#about">情报源</a></nav><div className="header-actions"><span className="live"><i/> 每日更新</span><a className="github" href="https://github.com/waxinigou-commits/AI-project-analysis" target="_blank" rel="noreferrer">GitHub ↗</a><button className="menu" onClick={()=>setMenuOpen(!menuOpen)} aria-label="打开导航">☰</button></div></header>
    {menuOpen && <div className="mobile-nav"><a href="#products">产品雷达</a><a href="#trends">趋势洞察</a><a href="#agent">Codex Agent</a><a href="#about">情报源</a></div>}
    <main>
      <section className="hero"><div><p className="eyebrow">AI COMMERCIAL INTELLIGENCE</p><h1>发现下一个<br/><em>商业信号</em></h1><p className="hero-copy">追踪全球 AI 新产品。原始事实逐条关联来源，商业判断明确标记为分析，不把推断伪装成事实。</p><div className="hero-actions"><a href="#agent">使用 Codex Agent ↓</a><a href="https://github.com/waxinigou-commits/AI-project-analysis/tree/main/skills/ai-product-growth-agent" target="_blank" rel="noreferrer">查看源码 ↗</a></div></div><div className="hero-side"><div className="pulse"><span>VERIFIED</span><div className="orb">{products.length}</div><p>已核验产品</p></div><div className="updated"><span>最后核验</span><b>{lastVerified}</b></div></div></section>

      <section className="metrics">
        <article><div><span>近 7 日核验</span><strong>{recentCount}</strong></div><Sparkline values={products.slice(0,7).map((_,i)=>i+1)}/><small>当前静态快照</small></article>
        <article><div><span>分析潜力均值</span><strong>{avg}</strong></div><Sparkline values={products.slice(0,7).map(p=>p.score)}/><small>分析分 ≥80 <b>{products.filter(p=>p.score>=80).length} 个</b></small></article>
        <article><div><span>当前样本热门赛道</span><strong>{catStats[0]?.name || "—"}</strong></div><div className="mini-bars">{catStats.map((x,i)=><i key={x.name} style={{height:`${30+(x.count/maxCat)*70}%`,background:COLORS[i%COLORS.length]}}/>)}</div><small>基于 {products.length} 条已核验记录</small></article>
        <article><div><span>配置采集源</span><strong>2</strong></div><div className="sources"><span>PH</span><span>WL</span></div><small>Product Hunt · WhatLaunched</small></article>
      </section>

      <section className="trends" id="trends"><div className="section-title"><div><p className="eyebrow">VERIFIED SAMPLE</p><h2>样本分布</h2></div><select value={period} onChange={e=>setPeriod(e.target.value)} aria-label="统计时间"><option>7 天</option><option>30 天</option><option>90 天</option></select></div><div className="trend-content"><div className="bar-chart">{catStats.map(x=><div className="bar-row" key={x.name}><span>{x.name}</span><div><i style={{width:`${(x.count/maxCat)*100}%`,background:x.color}}/><b>{x.count}</b></div></div>)}</div><div className="trend-note"><span>样本观察</span><strong>{catStats[0]?.name || "—"}</strong><p>在当前 {products.length} 条已核验静态记录中数量最多。这是样本分布，不等同于全市场趋势；扩大连续采集窗口后再进行趋势判断。</p><a href="#products">查看相关产品 ↓</a></div></div></section>

      <section className="radar" id="products"><div className="section-title"><div><p className="eyebrow">PRODUCT RADAR</p><h2>最新产品</h2></div><div className="view-count">{filtered.length} 个结果</div></div>
        <div className="filters"><label><Icon>⌕</Icon><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="搜索产品、定位或用户…"/></label><select className="time-filter" value={period} onChange={e=>setPeriod(e.target.value)} aria-label="产品发布时间"><option>7 天</option><option>30 天</option><option>90 天</option></select><div className="chips">{categories.map(c=><button key={c} className={category===c?"selected":""} onClick={()=>setCategory(c)}>{c}</button>)}</div></div>
        <div className="product-list">{filtered.map((p,i)=><article className="product-card" key={p.id} onClick={()=>setSelected(p)} tabIndex={0} onKeyDown={e=>e.key==="Enter"&&setSelected(p)}><ProductLogo name={p.name} index={i}/><div className="product-main"><div className="product-title"><h3>{p.name}</h3><span>{p.source}</span><span className="verified-badge">✓ {p.factStatus}</span></div><p>{p.tagline}</p><div className="tags"><span>{p.category}</span>{p.targetUsers.slice(0,2).map(x=><span key={x}>{x}</span>)}</div></div><div className="business"><span>分析 · 商业模式</span><b>{p.pricingModel}</b><small>{p.pricing}</small></div><div className="signals"><span>分析 · 增长信号</span>{p.signals.slice(0,2).map(x=><small key={x}>↗ {x}</small>)}</div><ScoreRing score={p.score}/><button className="arrow" aria-label={`查看 ${p.name}`}>→</button></article>)}</div>
        {!filtered.length && <div className="empty"><b>没有找到匹配的产品</b><p>换一个关键词或分类试试。</p></div>}
      </section>

      <section className="agent" id="agent">
        <div className="agent-copy"><p className="eyebrow">CODEX-NATIVE AGENT</p><h2>从发现新品，到生成增长内容</h2><p>安装公开 Skill 后，Codex 会读取公开 Feed、核验一手来源、区分事实与分析，并为不同平台制作待审核推广草稿。无需 <code>OPENAI_API_KEY</code>。</p><div className="agent-actions"><a className="primary" href="https://github.com/waxinigou-commits/AI-project-analysis/tree/main/skills/ai-product-growth-agent" target="_blank" rel="noreferrer">安装 Agent ↗</a><a href="https://github.com/waxinigou-commits/AI-project-analysis/blob/main/promotion/launch-kit.md" target="_blank" rel="noreferrer">查看推广包 ↗</a></div></div>
        <div className="agent-flow"><div><b>01</b><span>收集</span><small>Product Hunt · V2EX 公开 Feed</small></div><div><b>02</b><span>核验</span><small>官网 · 定价 · 发布记录</small></div><div><b>03</b><span>分析</span><small>定位 · 用户 · 商业模式</small></div><div><b>04</b><span>增长</span><small>多平台差异化推广草稿</small></div></div>
        <div className="agent-prompt"><span>在 Codex 中输入</span><code>使用 $ai-product-growth-agent 收集过去 24 小时的新 AI 产品，核验前 10 名，并为最值得关注的 3 个生成推广草稿；不要自动发布。</code><small>默认在发布前请求人工确认，不绕过验证码或平台风控。</small></div>
      </section>

      <section className="about" id="about"><div><p className="eyebrow">HOW IT WORKS</p><h2>从发布，到可行动的商业判断</h2></div><ol><li><b>01</b><span><strong>每日采集</strong>Product Hunt RSS 与 WhatLaunched 新品</span></li><li><b>02</b><span><strong>结构化分析</strong>定位、用户、竞品、定价与增长机会</span></li><li><b>03</b><span><strong>版本化入库</strong>SQLite 留存，JSON 快照驱动静态站点</span></li></ol></section>
    </main>
    <footer><Brand/><p>每天早一点，看见 AI 商业世界的变化。</p><span>数据仅供研究，不构成投资建议。</span></footer>
    {selected && <Detail product={selected} close={()=>setSelected(null)}/>} 
  </div>;
}
