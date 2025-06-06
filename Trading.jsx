import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { formatCurrency } from "@/lib/utils";

const Trading = () => {
  // Sample positions data
  const [positions, setPositions] = useState([
    {
      id: 1,
      symbol: "AAPL",
      side: "long",
      quantity: 10,
      entry_price: 180.5,
      current_price: 185.2,
      unrealized_pnl: 47.0,
    },
    {
      id: 2,
      symbol: "MSFT",
      side: "long",
      quantity: 5,
      entry_price: 320.75,
      current_price: 330.5,
      unrealized_pnl: 48.75,
    },
  ]);

  // Sample orders data
  const [orders, setOrders] = useState([
    {
      id: 1,
      symbol: "AAPL",
      order_type: "market",
      side: "buy",
      quantity: 10,
      price: null,
      status: "filled",
      created_at: "2023-05-15 10:30:45",
    },
    {
      id: 2,
      symbol: "MSFT",
      order_type: "market",
      side: "buy",
      quantity: 5,
      price: null,
      status: "filled",
      created_at: "2023-05-15 11:15:22",
    },
    {
      id: 3,
      symbol: "GOOGL",
      order_type: "limit",
      side: "buy",
      quantity: 3,
      price: 135.5,
      status: "pending",
      created_at: "2023-05-16 09:45:10",
    },
  ]);

  // Sample accounts data
  const [accounts, setAccounts] = useState([
    {
      id: 1,
      name: "Main Trading Account",
      broker: "Interactive Brokers",
      balance: 25000.0,
      equity: 25095.75,
      margin_used: 12500.0,
      is_active: true,
    },
  ]);

  const getOrderStatusBadge = (status) => {
    switch (status) {
      case "filled":
        return <Badge className="bg-green-500">Filled</Badge>;
      case "pending":
        return <Badge className="bg-blue-500">Pending</Badge>;
      case "cancelled":
        return <Badge className="bg-red-500">Cancelled</Badge>;
      case "rejected":
        return <Badge className="bg-red-500">Rejected</Badge>;
      default:
        return <Badge className="bg-gray-500">Unknown</Badge>;
    }
  };

  const getSideBadge = (side) => {
    switch (side) {
      case "buy":
      case "long":
        return <Badge className="bg-green-500">{side}</Badge>;
      case "sell":
      case "short":
        return <Badge className="bg-red-500">{side}</Badge>;
      default:
        return <Badge className="bg-gray-500">{side}</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Trading</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {accounts.map((account) => (
          <Card key={account.id}>
            <CardHeader>
              <div className="flex justify-between items-start">
                <CardTitle>{account.name}</CardTitle>
                <Badge variant={account.is_active ? "default" : "outline"}>
                  {account.is_active ? "Active" : "Inactive"}
                </Badge>
              </div>
              <CardDescription>{account.broker}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Balance:</span>
                  <span className="text-sm">{formatCurrency(account.balance)}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Equity:</span>
                  <span className="text-sm">{formatCurrency(account.equity)}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Margin Used:</span>
                  <span className="text-sm">{formatCurrency(account.margin_used)}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Tabs defaultValue="positions">
        <TabsList>
          <TabsTrigger value="positions">Positions</TabsTrigger>
          <TabsTrigger value="orders">Orders</TabsTrigger>
        </TabsList>
        <TabsContent value="positions">
          <Card>
            <CardHeader>
              <CardTitle>Open Positions</CardTitle>
              <CardDescription>
                Currently open positions in your account
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Symbol</TableHead>
                    <TableHead>Side</TableHead>
                    <TableHead>Quantity</TableHead>
                    <TableHead>Entry Price</TableHead>
                    <TableHead>Current Price</TableHead>
                    <TableHead>Unrealized P&L</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {positions.map((position) => (
                    <TableRow key={position.id}>
                      <TableCell className="font-medium">{position.symbol}</TableCell>
                      <TableCell>{getSideBadge(position.side)}</TableCell>
                      <TableCell>{position.quantity}</TableCell>
                      <TableCell>{formatCurrency(position.entry_price)}</TableCell>
                      <TableCell>{formatCurrency(position.current_price)}</TableCell>
                      <TableCell className={position.unrealized_pnl >= 0 ? "text-green-500" : "text-red-500"}>
                        {formatCurrency(position.unrealized_pnl)}
                      </TableCell>
                      <TableCell>
                        <Button variant="outline" size="sm">Close</Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="orders">
          <Card>
            <CardHeader>
              <CardTitle>Orders</CardTitle>
              <CardDescription>
                Recent and pending orders
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Symbol</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Side</TableHead>
                    <TableHead>Quantity</TableHead>
                    <TableHead>Price</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Created At</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {orders.map((order) => (
                    <TableRow key={order.id}>
                      <TableCell className="font-medium">{order.symbol}</TableCell>
                      <TableCell>{order.order_type}</TableCell>
                      <TableCell>{getSideBadge(order.side)}</TableCell>
                      <TableCell>{order.quantity}</TableCell>
                      <TableCell>{order.price ? formatCurrency(order.price) : "Market"}</TableCell>
                      <TableCell>{getOrderStatusBadge(order.status)}</TableCell>
                      <TableCell>{order.created_at}</TableCell>
                      <TableCell>
                        {order.status === "pending" && (
                          <Button variant="outline" size="sm">Cancel</Button>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Trading;

