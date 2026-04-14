import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

const EncounterCreator = () => {
  // UI State
  const [activeTab, setActiveTab] = useState('manual');
  const [loading, setLoading] = useState(true);
  const [results, setResults] = useState(null);

  // Data State
  const [allMonsters, setAllMonsters] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  // Form State (Matches your Pydantic model)
  const [playerInfo, setPlayerInfo] = useState({ count: 4, level: 1 });
  const [difficulty, setDifficulty] = useState('moderate');
  const [filters, setFilters] = useState({ type: '', size: '', alignment: '' });
  const [selectedMonsterNames, setSelectedMonsterNames] = useState([]);

  // Load monsters for the Manual Selection table
  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await api.getAllMonsters();
        setAllMonsters(data);
      } catch (err) {
        console.error("Failed to load bestiary");
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const handleToggleMonster = (name) => {
    setSelectedMonsterNames(prev => 
      prev.includes(name) ? prev.filter(n => n !== name) : [...prev, name]
    );
  };

  const handleGenerate = async () => {
    const payload = {
      difficulty: difficulty,
      players: {
        number_of_players: playerInfo.count,
        level: playerInfo.level
      },
      // Send names if in manual tab, otherwise send attributes
      monster_names: activeTab === 'manual' ? selectedMonsterNames : null,
      types: activeTab === 'filters' && filters.type ? [filters.type] : null,
      sizes: activeTab === 'filters' && filters.size ? [filters.size] : null,
      alignments: activeTab === 'filters' && filters.alignment ? [filters.alignment] : null,
    };

    try {
      const data = await api.generateEncounter(payload);
      setResults(data);
    } catch (err) {
      alert("Error generating encounter. Check console.");
    }
  };

  // Filter the 11k list down to a manageable view
  const visibleMonsters = allMonsters
    .filter(m => m.name.toLowerCase().includes(searchTerm.toLowerCase()))
    .slice(0, 15);

  return (
    <div className="p-6 max-w-5xl mx-auto font-sans text-gray-800">
      <header className="mb-8 border-b pb-4">
        <h1 className="text-3xl font-bold text-red-800">⚔️ Encounter Creator v0.1</h1>
        <p className="text-gray-600">Chronurgy Wizard's Workshop</p>
      </header>

      {/* 1. Global Player Settings */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 p-4 bg-slate-50 border rounded-lg">
        <div>
          <label className="block font-semibold mb-1">Difficulty</label>
          <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)} className="w-full border p-2 rounded">
            {['low', 'moderate', 'hard'].map(d => <option key={d} value={d}>{d}</option>)}
          </select>
        </div>
        <div>
          <label className="block font-semibold mb-1">Player Count</label>
          <select value={playerInfo.count} onChange={(e) => setPlayerInfo({...playerInfo, count: parseInt(e.target.value)})} className="w-full border p-2 rounded">
            {[1,2,3,4,5,6,7,8,9,10].map(n => <option key={n} value={n}>{n} Players</option>)}
          </select>
        </div>
        <div>
          <label className="block font-semibold mb-1">Average Level</label>
          <select value={playerInfo.level} onChange={(e) => setPlayerInfo({...playerInfo, level: parseInt(e.target.value)})} className="w-full border p-2 rounded">
            {Array.from({length: 20}, (_, i) => i + 1).map(lv => <option key={lv} value={lv}>Level {lv}</option>)}
          </select>
        </div>
      </section>

      {/* 2. Tabs */}
      <div className="flex space-x-2 mb-4">
        <button 
          onClick={() => setActiveTab('manual')}
          className={`px-4 py-2 rounded-t-lg border-t border-l border-r ${activeTab === 'manual' ? 'bg-white font-bold text-blue-700' : 'bg-gray-200'}`}
        >
          Manual Selection
        </button>
        <button 
          onClick={() => setActiveTab('filters')}
          className={`px-4 py-2 rounded-t-lg border-t border-l border-r ${activeTab === 'filters' ? 'bg-white font-bold text-blue-700' : 'bg-gray-200'}`}
        >
          Vague Filters
        </button>
      </div>

      {/* 3. Tab Content */}
      <div className="bg-white border p-6 rounded-b-lg rounded-tr-lg shadow-sm mb-8">
        {activeTab === 'manual' ? (
          <div>
            <input 
              type="text" 
              placeholder="Search 11,000+ monsters..." 
              className="w-full border p-2 mb-4 rounded italic"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="p-2">Add</th>
                    <th className="p-2">Monster Name</th>
                    <th className="p-2">Type</th>
                    <th className="p-2">CR</th>
                  </tr>
                </thead>
                <tbody>
                  {visibleMonsters.map(m => (
                    <tr key={m.name} className="border-b hover:bg-blue-50">
                      <td className="p-2">
                        <input 
                          type="checkbox" 
                          checked={selectedMonsterNames.includes(m.name)}
                          onChange={() => handleToggleMonster(m.name)}
                        />
                      </td>
                      <td className="p-2 font-medium">{m.name}</td>
                      <td className="p-2 text-gray-600">{m.type}</td>
                      <td className="p-2 text-sm">{m.challenge_rating}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <p className="text-xs text-gray-400 mt-2">Showing top {visibleMonsters.length} matches.</p>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input 
              placeholder="Type (e.g. Beast, Undead)" 
              className="border p-2 rounded"
              value={filters.type}
              onChange={(e) => setFilters({...filters, type: e.target.value})}
            />
            <input 
              placeholder="Size (e.g. Large, Medium)" 
              className="border p-2 rounded"
              value={filters.size}
              onChange={(e) => setFilters({...filters, size: e.target.value})}
            />
             <input 
              placeholder="Alignment (e.g. Lawful Good)" 
              className="border p-2 rounded"
              value={filters.alignment}
              onChange={(e) => setFilters({...filters, alignment: e.target.value})}
            />
          </div>
        )}
      </div>

      {/* 4. Action */}
      <div className="text-center">
        <button 
          onClick={handleGenerate}
          className="bg-red-800 text-white px-10 py-3 rounded-full font-bold text-lg hover:bg-red-900 transition-colors shadow-lg"
        >
          Generate Encounter
        </button>
      </div>

      {/* 5. Results Section */}
      {results && (
        <div className="mt-12 p-6 bg-green-50 border-2 border-green-200 rounded-xl">
          <h2 className="text-2xl font-bold text-green-800 mb-4">Encounter Ready!</h2>
          <pre className="bg-white p-4 rounded border text-sm overflow-auto">
            {JSON.stringify(results, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default EncounterCreator;