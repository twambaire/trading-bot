import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ArrowUpRight, ArrowDownRight, TrendingUp, LineChart as LineChartIcon, Wallet } from "lucide-react";

const Dashboard = () => {
  // Sample data for charts
  const equityData = [
    { date: '2023-01', value: 10000 },
    { date: '2023-02', value: 10500 },
    { date: '2023-03', value: 10300 },
    { date: '2023-04', value: 11000 },
    { date: '2023-05', value: 10800 },
    { date: '2023-06', value: 11500 },
    { date: '2023-07', value: 12000 },
    { date: '2023-08', value: 12500 },
    { date: '2023-09', value: 12300 },
    { date: '2023-10', value: 13000 },
    { date: '2023-11', value: 13500 },
    { date: '2023-12', value: 14000 },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Balance</CardTitle>
            <Wallet className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$14,000.00</div>
            <div className="flex items-center pt-1 text-sm text-green-500">
              <ArrowUpRight className="mr-1 h-4 w-4" />
              <span>+15.3%</span>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Active Strategies</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
            <div className="pt-1 text-sm text-muted-foreground">
              5 total strategies
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Monthly Return</CardTitle>
            <LineChartIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">+3.7%</div>
            <div className="flex items-center pt-1 text-sm text-green-500">
              <ArrowUpRight className="mr-1 h-4 w-4" />
              <span>+2.5%</span>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Drawdown</CardTitle>
            <LineChartIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">-5.2%</div>
            <div className="flex items-center pt-1 text-sm text-red-500">
              <ArrowDownRight className="mr-1 h-4 w-4" />
              <span>+1.2%</span>
            </div>
          </CardContent>
        </Card>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Equity Curve</CardTitle>
          <CardDescription>Your account performance over time</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={equityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  stroke="var(--color-primary)" 
                  strokeWidth={2} 
                  dot={false} 
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;

