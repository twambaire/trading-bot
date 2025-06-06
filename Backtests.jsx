import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Plus, LineChart, FileText, Trash2, Play } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { formatPercent } from "@/lib/utils";

const Backtests = () => {
  // Sample backtests data
  const [backtests, setBacktests] = useState([
    {
      id: 1,
      name: "MA Crossover - AAPL 2023",
      description: "Moving Average Crossover strategy on AAPL for 2023",
      strategy: "Moving Average Crossover",
      symbol: "AAPL",
      start_date: "2023-01-01",
      end_date: "2023-12-31",
      status: "completed",
      metrics: {
        total_return: 15.3,
        annual_return: 15.3,
        sharpe_ratio: 1.2,
        max_drawdown: 5.2,
        win_rate: 65.0,
      },
    },
    {
      id: 2,
      name: "RSI Strategy - MSFT 2023",
      description: "RSI strategy on MSFT for 2023",
      strategy: "RSI Strategy",
      symbol: "MSFT",
      start_date: "2023-01-01",
      end_date: "2023-12-31",
      status: "completed",
      metrics: {
        total_return: 12.7,
        annual_return: 12.7,
        sharpe_ratio: 1.1,
        max_drawdown: 6.5,
        win_rate: 60.0,
      },
    },
    {
      id: 3,
      name: "MACD Strategy - GOOGL 2023",
      description: "MACD strategy on GOOGL for 2023",
      strategy: "MACD Strategy",
      symbol: "GOOGL",
      start_date: "2023-01-01",
      end_date: "2023-12-31",
      status: "running",
      metrics: null,
    },
  ]);

  const getStatusBadge = (status) => {
    switch (status) {
      case "completed":
        return <Badge className="bg-green-500">Completed</Badge>;
      case "running":
        return <Badge className="bg-blue-500">Running</Badge>;
      case "failed":
        return <Badge className="bg-red-500">Failed</Badge>;
      default:
        return <Badge className="bg-gray-500">Pending</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Backtests</h1>
        <Button>
          <Plus className="mr-2 h-4 w-4" /> New Backtest
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Backtests</CardTitle>
          <CardDescription>
            View and manage your backtest results
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Strategy</TableHead>
                <TableHead>Symbol</TableHead>
                <TableHead>Period</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Return</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {backtests.map((backtest) => (
                <TableRow key={backtest.id}>
                  <TableCell className="font-medium">{backtest.name}</TableCell>
                  <TableCell>{backtest.strategy}</TableCell>
                  <TableCell>{backtest.symbol}</TableCell>
                  <TableCell>
                    {backtest.start_date} to {backtest.end_date}
                  </TableCell>
                  <TableCell>{getStatusBadge(backtest.status)}</TableCell>
                  <TableCell>
                    {backtest.metrics ? formatPercent(backtest.metrics.total_return) : "-"}
                  </TableCell>
                  <TableCell>
                    <div className="flex space-x-2">
                      {backtest.status === "completed" && (
                        <>
                          <Button variant="outline" size="icon">
                            <LineChart className="h-4 w-4" />
                          </Button>
                          <Button variant="outline" size="icon">
                            <FileText className="h-4 w-4" />
                          </Button>
                        </>
                      )}
                      {backtest.status === "pending" && (
                        <Button variant="outline" size="icon">
                          <Play className="h-4 w-4" />
                        </Button>
                      )}
                      <Button variant="outline" size="icon">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

export default Backtests;

