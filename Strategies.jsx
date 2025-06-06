import { useState } from "react";
import { useStrategies } from "@/hooks/useStrategies";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Plus, Edit, Trash2 } from "lucide-react";
import { Switch } from "@/components/ui/switch";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

const Strategies = () => {
  const { strategies, loading, error, updateStrategy, deleteStrategy } = useStrategies();
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [strategyToDelete, setStrategyToDelete] = useState(null);

  // Toggle strategy active state
  const toggleStrategyActive = async (id, isActive) => {
    try {
      const strategy = strategies.find((s) => s.id === id);
      await updateStrategy(id, { ...strategy, active: !isActive });
    } catch (error) {
      console.error("Failed to update strategy:", error);
      // In a real app, you would show an error notification here
    }
  };

  // Handle delete strategy
  const handleDeleteClick = (strategy) => {
    setStrategyToDelete(strategy);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = async () => {
    if (strategyToDelete) {
      try {
        await deleteStrategy(strategyToDelete.id);
        setDeleteDialogOpen(false);
        setStrategyToDelete(null);
      } catch (error) {
        console.error("Failed to delete strategy:", error);
        // In a real app, you would show an error notification here
      }
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 text-red-500 rounded-md">
        Error loading strategies: {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Strategies</h1>
        <Button>
          <Plus className="mr-2 h-4 w-4" /> New Strategy
        </Button>
      </div>

      {strategies.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center h-64">
            <p className="text-muted-foreground mb-4">No strategies found</p>
            <Button>
              <Plus className="mr-2 h-4 w-4" /> Create your first strategy
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {strategies.map((strategy) => (
            <Card key={strategy.id}>
              <CardHeader>
                <div className="flex justify-between items-start">
                  <CardTitle>{strategy.name}</CardTitle>
                  <Badge variant={strategy.active ? "default" : "outline"}>
                    {strategy.active ? "Active" : "Inactive"}
                  </Badge>
                </div>
                <CardDescription>{strategy.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Type:</span>
                    <span className="text-sm">{strategy.type}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Parameters:</span>
                    <span className="text-sm">{Object.keys(strategy.parameters || {}).length}</span>
                  </div>
                </div>
              </CardContent>
              <CardFooter className="flex justify-between">
                <div className="flex items-center space-x-2">
                  <Switch
                    checked={strategy.active}
                    onCheckedChange={() => toggleStrategyActive(strategy.id, strategy.active)}
                  />
                  <span className="text-sm">
                    {strategy.active ? "Active" : "Inactive"}
                  </span>
                </div>
                <div className="flex space-x-2">
                  <Button variant="outline" size="icon">
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button 
                    variant="outline" 
                    size="icon"
                    onClick={() => handleDeleteClick(strategy)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}

      <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This will permanently delete the strategy "{strategyToDelete?.name}".
              This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={confirmDelete} className="bg-red-500 hover:bg-red-600">
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default Strategies;

