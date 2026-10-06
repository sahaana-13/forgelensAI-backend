import StatusBadge from './StatusBadge';
export default function StatementComparison({items=[]}){return <div className="table-wrap"><table><thead><tr><th>Parameter</th><th>Party A</th><th>Party B</th><th>Status</th></tr></thead><tbody>{items.map((x,i)=><tr key={i}><td>{x.field}</td><td>{x.party_a}</td><td>{x.party_b}</td><td><StatusBadge>{x.status}</StatusBadge></td></tr>)}</tbody></table></div>}
