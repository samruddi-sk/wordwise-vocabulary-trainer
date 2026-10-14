import { useCallback, useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { BookOpen, CalendarDays, Check, ChevronRight, CircleHelp, Flame, Languages, Plus, RotateCcw, Trash2, TrendingUp, X } from 'lucide-react';

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000', timeout: 8000 });
const dateLabel = (value) => value ? new Date(`${value.slice(0, 10)}T12:00:00`).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' }) : 'Not scheduled';

export default function App() {
  const [tab, setTab] = useState('Study');
  const [due, setDue] = useState([]);
  const [history, setHistory] = useState({ total_words: 0, total_reviews: 0, accuracy_percent: 0, streak_days: 0, schedule: [], difficult_words: [], recent_reviews: [] });
  const [form, setForm] = useState({ word: '', definition: '', language: 'English' });
  const [showForm, setShowForm] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  const refresh = useCallback(async () => {
    try {
      setError('');
      const [dueResponse, historyResponse] = await Promise.all([api.get('/words/due/'), api.get('/words/history/')]);
      setDue(dueResponse.data);
      setHistory(historyResponse.data);
    } catch {
      setError('Could not connect to the API. Start the FastAPI backend on port 8000, then click Retry.');
    }
  }, []);
  useEffect(() => { refresh(); }, [refresh]);

  const currentWord = due[0];
  const addWord = async (event) => {
    event.preventDefault();
    setBusy(true); setNotice(''); setError('');
    try {
      await api.post('/words/', form);
      setForm({ word: '', definition: '', language: 'English' });
      setShowForm(false); setNotice('Word added to your vocabulary.'); await refresh(); setTab('Study');
    } catch (e) { setError(e.response?.data?.detail?.[0]?.msg || e.response?.data?.detail || 'Could not add this word. Check the fields and try again.'); }
    finally { setBusy(false); }
  };
  const submitReview = async (score) => {
    if (!currentWord) return;
    setBusy(true); setNotice(''); setError('');
    try {
      const response = await api.post(`/words/${currentWord.id}/review/`, { score });
      setNotice(`Saved: “${currentWord.word}” will return ${score <= 2 ? 'tomorrow' : `in ${response.data.interval} day${response.data.interval === 1 ? '' : 's'}`}.`);
      await refresh();
    } catch { setError('Could not save the review. Please try again.'); }
    finally { setBusy(false); }
  };
  const deleteWord = async (id) => {
    if (!window.confirm('Delete this vocabulary word and its review history?')) return;
    try { await api.delete(`/words/${id}`); setNotice('Word deleted.'); await refresh(); }
    catch { setError('Could not delete the word. Please try again.'); }
  };

  const nav = [ { name: 'Study', icon: BookOpen }, { name: 'My words', icon: Languages }, { name: 'Schedule', icon: CalendarDays }, { name: 'Progress', icon: TrendingUp } ];
  const schedule = useMemo(() => history.schedule || [], [history.schedule]);

  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-mark"><BookOpen size={20}/></div><div><strong>wordwise</strong><span>VOCABULARY STUDIO</span></div></div>
      <div className="nav-label">WORKSPACE</div>
      <nav>{nav.map(({name, icon: Icon}) => <button key={name} className={`nav-item ${tab === name ? 'active' : ''}`} onClick={() => { setTab(name); setShowForm(false); }}><Icon size={18}/><span>{name}</span>{name === 'Study' && due.length > 0 && <em>{due.length}</em>}</button>)}</nav>
      <div className="sidebar-bottom"><div className="daily-card"><div className="daily-icon"><Flame size={17}/></div><div><strong>{history.streak_days} day streak</strong><p>Small steps add up.</p></div></div><div className="sidebar-foot">A little practice, every day.</div></div>
    </aside>
    <main className="main-content">
      <header className="topbar"><div className="breadcrumb">Workspace <ChevronRight size={14}/> <strong>{tab}</strong></div><button className="primary-btn compact" onClick={() => { setShowForm(v => !v); setTab('My words'); }}><Plus size={16}/> Add a word</button></header>
      <div className="page-wrap">
        <div className="page-heading"><div><div className="eyebrow">YOUR PERSONAL LEARNING SPACE</div><h1>{tab === 'Study' ? 'Ready to remember more?' : tab === 'My words' ? 'Your vocabulary' : tab === 'Schedule' ? 'Review schedule' : 'Your progress'}</h1><p>{tab === 'Study' ? 'A few focused minutes today go a long way.' : tab === 'My words' ? 'Every word you collect is a new connection.' : tab === 'Schedule' ? 'See what is coming up and plan your next session.' : 'Notice the progress you are making, one word at a time.'}</p></div><div className="date-chip"><CalendarDays size={15}/>{new Date().toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })}</div></div>
        {error && <div className="alert error"><CircleHelp size={17}/><span>{error}</span><button onClick={refresh}>Retry</button></div>}
        {notice && <div className="alert success"><Check size={17}/><span>{notice}</span><button aria-label="Dismiss" onClick={() => setNotice('')}><X size={15}/></button></div>}
        <section className="stats-grid"><Stat label="Total words" value={history.total_words} detail="In your collection" icon={<BookOpen size={18}/>} /><Stat label="Reviews completed" value={history.total_reviews} detail="Keep the rhythm" icon={<RotateCcw size={18}/>} /><Stat label="Recall accuracy" value={`${history.accuracy_percent}%`} detail="Scores of 3–5 count" icon={<TrendingUp size={18}/>} /><Stat label="Day streak" value={history.streak_days} detail="Consecutive study days" icon={<Flame size={18}/>} /></section>

        {tab === 'Study' && <section className="study-layout"><div className="study-main"><div className="section-title"><div><h2>Due for review <span className="count-pill">{due.length}</span></h2><p>Rate how well you remembered this word.</p></div><button className="text-btn" onClick={refresh}><RotateCcw size={14}/> Refresh</button></div>
          {currentWord ? <div className="flashcard"><div className="card-top"><span className="language-pill"><Languages size={13}/>{currentWord.language}</span><span className="card-count">WORD {1} <span>/</span> {due.length}</span></div><div className="word-center"><div className="word-symbol">Aa</div><h2>{currentWord.word}</h2><p>{currentWord.definition}</p><span className="hint">How well did you remember it?</span></div><div className="score-grid">{[{score:0,label:'Forgot',sub:'No recall'},{score:1,label:'Hard',sub:'Barely recalled'},{score:2,label:'Difficult',sub:'Needed help'},{score:3,label:'Okay',sub:'With effort'},{score:4,label:'Good',sub:'Remembered'},{score:5,label:'Easy',sub:'Instant recall'}].map(item => <button disabled={busy} key={item.score} className={`score-btn score-${item.score}`} onClick={() => submitReview(item.score)}><strong>{item.score}</strong><span>{item.label}</span><small>{item.sub}</small></button>)}</div><div className="card-note">Your rating sets the next review date automatically.</div></div> : <div className="empty-state"><div className="empty-icon"><Check size={26}/></div><h3>You're all caught up!</h3><p>No words are due right now. Add a new word or check your upcoming schedule.</p><button className="primary-btn" onClick={() => { setTab('My words'); setShowForm(true); }}><Plus size={16}/> Add your first word</button></div>}
          </div><aside className="side-panel"><div className="panel-head"><div><h3>Coming up</h3><p>Your next review sessions</p></div><CalendarDays size={18}/></div>{schedule.length ? schedule.slice(0,5).map(item => <div className="upcoming-row" key={item.id}><div className="upcoming-dot"/><div className="upcoming-info"><strong>{item.word}</strong><span>{item.language}</span></div><time>{dateLabel(item.next_review)}</time></div>) : <div className="panel-empty">Your schedule will appear here after your first review.</div>}<button className="panel-link" onClick={() => setTab('Schedule')}>View full schedule <ChevronRight size={15}/></button><div className="tip-card"><div className="tip-icon">✦</div><div><strong>Learning tip</strong><p>Try saying the definition out loud before you reveal it. Active recall helps words stick.</p></div></div></aside></section>}

        {tab === 'My words' && <section className="content-panel"><div className="section-title"><div><h2>All vocabulary</h2><p>Manage the words you are learning.</p></div><button className="primary-btn compact" onClick={() => setShowForm(v => !v)}><Plus size={15}/>{showForm ? 'Close form' : 'Add a word'}</button></div>
          {showForm && <form className="word-form" onSubmit={addWord}><label>Word<input required maxLength="200" value={form.word} onChange={e => setForm({...form, word:e.target.value})} placeholder="e.g. bonjour"/></label><label>Definition<input required maxLength="2000" value={form.definition} onChange={e => setForm({...form, definition:e.target.value})} placeholder="What does it mean?"/></label><label>Language<input required maxLength="80" value={form.language} onChange={e => setForm({...form, language:e.target.value})} placeholder="e.g. French"/></label><button className="primary-btn" disabled={busy} type="submit">{busy ? 'Saving…' : 'Save word'}</button></form>}
          {schedule.length ? <div className="word-list">{schedule.map(item => <div className="word-row" key={item.id}><div className="word-avatar">{item.word.slice(0,1).toUpperCase()}</div><div className="word-main"><strong>{item.word}</strong><p>{item.definition}</p></div><span className="language-tag">{item.language}</span><span className={`status-tag ${item.is_due ? 'is-due' : ''}`}>{item.is_due ? 'Due now' : `Next: ${dateLabel(item.next_review)}`}</span><button className="icon-btn danger" aria-label={`Delete ${item.word}`} onClick={() => deleteWord(item.id)}><Trash2 size={16}/></button></div>)}</div> : !showForm && <div className="empty-inline">No words yet. Add your first vocabulary word to get started.</div>}
        </section>}

        {tab === 'Schedule' && <section className="content-panel"><div className="section-title"><div><h2>Upcoming reviews</h2><p>Words are sorted by their next scheduled review.</p></div></div>{schedule.length ? <div className="schedule-list">{schedule.map(item => <div className="schedule-row" key={item.id}><div className="schedule-date"><strong>{item.next_review ? new Date(`${item.next_review.slice(0,10)}T12:00:00`).toLocaleDateString(undefined,{day:'2-digit'}) : '—'}</strong><span>{item.next_review ? new Date(`${item.next_review.slice(0,10)}T12:00:00`).toLocaleDateString(undefined,{month:'short'}) : 'No date'}</span></div><div className="schedule-detail"><strong>{item.word}</strong><p>{item.definition}</p><span>{item.language}</span></div><span className={`status-tag ${item.is_due ? 'is-due' : ''}`}>{item.is_due ? 'Due now' : 'Scheduled'}</span></div>)}</div> : <div className="empty-inline">Review a word to start building your schedule.</div>}</section>}

        {tab === 'Progress' && <section className="progress-layout"><div className="content-panel"><div className="section-title"><div><h2>Words to revisit</h2><p>Words with your lowest recent scores.</p></div></div>{history.difficult_words?.length ? history.difficult_words.map(item => <div className="difficult-row" key={item.id}><div><strong>{item.word}</strong><p>{item.definition}</p></div><span className="score-badge">Last score: {item.last_score}/5</span></div>) : <div className="empty-inline">Your difficult words will show up after you start reviewing.</div>}</div><div className="content-panel"><div className="section-title"><div><h2>Recent reviews</h2><p>Your latest learning activity.</p></div></div>{history.recent_reviews?.length ? history.recent_reviews.slice(0,10).map(item => { const word = schedule.find(w => w.id === item.word_id); return <div className="review-row" key={item.id}><div className="review-check"><Check size={14}/></div><div><strong>{word?.word || `Word #${item.word_id}`}</strong><p>{dateLabel(item.review_date)}</p></div><span className="review-score">{item.score}/5</span></div>; }) : <div className="empty-inline">Your review history will appear here.</div>}</div></section>}
        <footer className="footer-note">Built for consistent learning <span>·</span> Powered by spaced repetition</footer>
      </div>
    </main>
  </div>;
}

function Stat({label, value, detail, icon}) { return <div className="stat-card"><div className="stat-top"><span>{label}</span><div className="stat-icon">{icon}</div></div><strong className="stat-value">{value}</strong><small>{detail}</small></div>; }
