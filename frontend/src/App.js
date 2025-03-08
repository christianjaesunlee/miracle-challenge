import React, { useEffect, useState } from 'react';
import {
    BarChart, Bar, LineChart, Line, Legend, XAxis, YAxis, Tooltip, CartesianGrid, LabelList,
    PieChart, Pie, Cell, ResponsiveContainer
} from 'recharts';

function App() {
    // State for sponsor bar chart
    const [barData, setBarData] = useState([]);
    // State for condition pie chart
    const [pieData, setPieData] = useState([]);
    // State for us total
    const [usTotal, setUsTotal] = useState([]);
    // State for eu total
    const [euTotal, setEuTotal] = useState([]);
    // State for past week total
    const [weekTotal, setWeekTotal] = useState([]);

    useEffect(() => {
        fetch('http://localhost:5000/api/sponsor?limit=20') // limit number of sponsors shown to top 20 plus "other"
            .then(response => response.json())
            .then(data => {
                setBarData(data);
            })
            .catch(err => console.error("Error fetching sponsor data:", err));


        fetch('http://localhost:5000/api/condition')
            .then(response => response.json())
            .then(data => {
                setPieData(data);
            })
            .catch(err => console.error("Error fetching condition data:", err));

        fetch('http://localhost:5000/api/us_count')
            .then(response => response.json())
            .then(data => {
                setUsTotal(data);
            })
            .catch(err => console.error("Error fetching us total count:", err));

        fetch('http://localhost:5000/api/eu_count')
            .then(response => response.json())
            .then(data => {
                setEuTotal(data);
            })
            .catch(err => console.error("Error fetching eu total count:", err));

        fetch('http://localhost:5000/api/compare_week')
            .then(response => response.json())
            .then(data => {
                setWeekTotal(data);
            })
            .catch(err => console.error("Error fetching week total data:", err));
    }, []);

    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AA46BE', '#FF6699'];

    return (
        <div style={{ textAlign: 'center', width: '100%', height: '400px' }}>
            <h1>Miracle Challenge</h1>
            <p>Total US count: {usTotal}</p>
            <p>Total EU count: {euTotal}</p>

            <h2>Clinical Trials by Sponsor</h2>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart
                    data={barData}
                    margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#8884d8">
                        <LabelList dataKey="value" position="top" />
                    </Bar>
                </BarChart>
            </ResponsiveContainer>

            <h2>Clinical Trials by Condition</h2>
            <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                    <Pie
                        data={pieData}
                        dataKey="value"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        outerRadius={120}
                        fill="#8884d8"
                        label
                    >
                        {pieData.map((entry, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={COLORS[index % COLORS.length]}
                            />
                        ))}
                    </Pie>
                    <Tooltip />
                </PieChart>
            </ResponsiveContainer>

            <h2>Total count over past week</h2>
            <ResponsiveContainer width="100%" height="100%">
                <LineChart
                    width={500}
                    height={300}
                    data={weekTotal}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="snapshot_date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="trial_count" stroke="#8884d8" activeDot={{ r: 8 }} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}

export default App;
