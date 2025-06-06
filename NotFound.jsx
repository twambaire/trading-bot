import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { AlertCircle } from "lucide-react";

const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-background p-4">
      <div className="text-center space-y-6 max-w-md">
        <div className="flex justify-center">
          <AlertCircle className="h-24 w-24 text-muted-foreground" />
        </div>
        <h1 className="text-4xl font-bold">404 - Page Not Found</h1>
        <p className="text-muted-foreground text-lg">
          The page you are looking for doesn't exist or has been moved.
        </p>
        <Button asChild size="lg">
          <Link to="/">Return to Dashboard</Link>
        </Button>
      </div>
    </div>
  );
};

export default NotFound;

