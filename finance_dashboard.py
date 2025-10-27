import React, { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { PieChart, Pie, Cell, Tooltip, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

export default function BudgetTracker() {
  const [budget, setBudget] = useState('');
  const [balance, setBalance] = useState(0);
  const [income, setIncome] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [type, setType] = useState('Expense');
  const [category, setCategory] = useState('');
  const [amount, setAmount] = useState('');

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AA336A'];

  const handleSetBudget = () => {
    if (!budget || budget <= 0) return alert('Please enter a valid budget');
    setBalance(parseFloat(budget));
  };

  const handleAdd = () => {
    const amt = parseFloat(amount);
    if (!category || amt <= 0) return alert('Enter valid details');

    if (type === 'Expense') {
      if (amt > balance) return alert('Not enough balance!');
      const updated = [...expenses, { category, amount: amt }];
      setExpenses(updated);
      setBalance(balance - amt);
    } else {
      const updated = [...income, { category, amount: amt }];
      setIncome(updated);
      setBalance(balance + amt);
    }

    setCategory('');
    setAmount('');
  };

  const totalIncome = income.reduce((a, b) => a + b.amount, 0);
  const totalExpense = expenses.reduce((a, b) => a + b.amount, 0);

  return (
    <div className="p-6 flex flex-col items-center space-y-6 bg-gray-100 min-h-screen">
      <Card className="w-full max-w-md shadow-xl">
        <CardContent className="space-y-4 p-6">
          <h1 className="text-2xl font-bold text-center">💰 Smart Budget Tracker</h1>

          {!balance ? (
            <div className="space-y-3">
              <Input
                type="number"
                placeholder="Enter total budget"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
              />
              <Button className="w-full" onClick={handleSetBudget}>Set Budget</Button>
            </div>
          ) : (
            <>
              <div className="text-center">
                <p className="text-lg font-semibold">Total Budget: ₹{budget}</p>
                <p className={`text-lg font-bold ${balance < 0 ? 'text-red-600' : 'text-green-600'}`}>
                  Remaining Balance: ₹{balance}
                </p>
              </div>

              <div className="space-y-3">
                <select
                  className="w-full p-2 border rounded"
                  value={type}
                  onChange={(e) => setType(e.target.value)}
                >
                  <option>Expense</option>
                  <option>Income</option>
                </select>

                <Input
                  type="text"
                  placeholder="Category (e.g. Food, Rent, Salary)"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                />

                <Input
                  type="number"
                  placeholder="Amount"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                />

                <Button className="w-full" onClick={handleAdd}>Add {type}</Button>
              </div>
            </>
          )}
        </CardContent>
      </Card>

      {(expenses.length > 0 || income.length > 0) && (
        <div className="w-full max-w-2xl grid grid-cols-1 md:grid-cols-2 gap-6">
          {expenses.length > 0 && (
            <Card className="shadow-md">
              <CardContent className="p-4">
                <h2 className="text-lg font-bold text-center">Expense Breakdown</h2>
                <PieChart width={300} height={250}>
                  <Pie data={expenses} dataKey="amount" nameKey="category" cx="50%" cy="50%" outerRadius={80}>
                    {expenses.map((_, index) => (
                      <Cell key={index} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </CardContent>
            </Card>
          )}

          <Card className="shadow-md">
            <CardContent className="p-4">
              <h2 className="text-lg font-bold text-center">Income vs Expense</h2>
              <BarChart width={300} height={250} data={[{ name: 'Total', Income: totalIncome, Expense: totalExpense }]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="Income" fill="#00C49F" />
                <Bar dataKey="Expense" fill="#FF8042" />
              </BarChart>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
