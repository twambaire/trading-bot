import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Switch } from "@/components/ui/switch";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const Settings = () => {
  const [generalSettings, setGeneralSettings] = useState({
    username: "johndoe",
    email: "john.doe@example.com",
    notifications: true,
  });

  const [tradingSettings, setTradingSettings] = useState({
    defaultRisk: 1,
    maxDrawdown: 10,
    tradingHours: "market",
  });

  const [apiSettings, setApiSettings] = useState({
    broker: "interactive_brokers",
    apiKey: "••••••••••••••••",
    apiSecret: "••••••••••••••••",
  });

  const handleGeneralSettingsChange = (e) => {
    const { name, value } = e.target;
    setGeneralSettings({
      ...generalSettings,
      [name]: value,
    });
  };

  const handleTradingSettingsChange = (e) => {
    const { name, value } = e.target;
    setTradingSettings({
      ...tradingSettings,
      [name]: value,
    });
  };

  const handleApiSettingsChange = (e) => {
    const { name, value } = e.target;
    setApiSettings({
      ...apiSettings,
      [name]: value,
    });
  };

  const handleNotificationsChange = (checked) => {
    setGeneralSettings({
      ...generalSettings,
      notifications: checked,
    });
  };

  const handleTradingHoursChange = (value) => {
    setTradingSettings({
      ...tradingSettings,
      tradingHours: value,
    });
  };

  const handleBrokerChange = (value) => {
    setApiSettings({
      ...apiSettings,
      broker: value,
    });
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Settings</h1>

      <Tabs defaultValue="general">
        <TabsList>
          <TabsTrigger value="general">General</TabsTrigger>
          <TabsTrigger value="trading">Trading</TabsTrigger>
          <TabsTrigger value="api">API Connections</TabsTrigger>
        </TabsList>
        
        <TabsContent value="general">
          <Card>
            <CardHeader>
              <CardTitle>General Settings</CardTitle>
              <CardDescription>
                Manage your account settings and preferences
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  name="username"
                  value={generalSettings.username}
                  onChange={handleGeneralSettingsChange}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={generalSettings.email}
                  onChange={handleGeneralSettingsChange}
                />
              </div>
              <div className="flex items-center space-x-2">
                <Switch
                  id="notifications"
                  checked={generalSettings.notifications}
                  onCheckedChange={handleNotificationsChange}
                />
                <Label htmlFor="notifications">Enable notifications</Label>
              </div>
            </CardContent>
            <CardFooter>
              <Button>Save Changes</Button>
            </CardFooter>
          </Card>
        </TabsContent>
        
        <TabsContent value="trading">
          <Card>
            <CardHeader>
              <CardTitle>Trading Settings</CardTitle>
              <CardDescription>
                Configure your trading parameters and risk management
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="defaultRisk">Default Risk (%)</Label>
                <Input
                  id="defaultRisk"
                  name="defaultRisk"
                  type="number"
                  min="0.1"
                  max="10"
                  step="0.1"
                  value={tradingSettings.defaultRisk}
                  onChange={handleTradingSettingsChange}
                />
                <p className="text-sm text-muted-foreground">
                  Percentage of account balance to risk per trade
                </p>
              </div>
              <div className="space-y-2">
                <Label htmlFor="maxDrawdown">Maximum Drawdown (%)</Label>
                <Input
                  id="maxDrawdown"
                  name="maxDrawdown"
                  type="number"
                  min="1"
                  max="50"
                  step="1"
                  value={tradingSettings.maxDrawdown}
                  onChange={handleTradingSettingsChange}
                />
                <p className="text-sm text-muted-foreground">
                  Maximum allowed drawdown before stopping trading
                </p>
              </div>
              <div className="space-y-2">
                <Label htmlFor="tradingHours">Trading Hours</Label>
                <Select
                  value={tradingSettings.tradingHours}
                  onValueChange={handleTradingHoursChange}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select trading hours" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="market">Market Hours Only</SelectItem>
                    <SelectItem value="extended">Extended Hours</SelectItem>
                    <SelectItem value="24h">24/7 Trading</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
            <CardFooter>
              <Button>Save Changes</Button>
            </CardFooter>
          </Card>
        </TabsContent>
        
        <TabsContent value="api">
          <Card>
            <CardHeader>
              <CardTitle>API Connections</CardTitle>
              <CardDescription>
                Configure your broker API connections
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="broker">Broker</Label>
                <Select
                  value={apiSettings.broker}
                  onValueChange={handleBrokerChange}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select broker" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="interactive_brokers">Interactive Brokers</SelectItem>
                    <SelectItem value="alpaca">Alpaca</SelectItem>
                    <SelectItem value="td_ameritrade">TD Ameritrade</SelectItem>
                    <SelectItem value="oanda">Oanda</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="apiKey">API Key</Label>
                <Input
                  id="apiKey"
                  name="apiKey"
                  type="password"
                  value={apiSettings.apiKey}
                  onChange={handleApiSettingsChange}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="apiSecret">API Secret</Label>
                <Input
                  id="apiSecret"
                  name="apiSecret"
                  type="password"
                  value={apiSettings.apiSecret}
                  onChange={handleApiSettingsChange}
                />
              </div>
            </CardContent>
            <CardFooter>
              <Button>Save Changes</Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Settings;

