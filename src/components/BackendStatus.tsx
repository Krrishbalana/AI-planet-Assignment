import { useEffect, useState } from "react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { CheckCircle2, XCircle, Loader2 } from "lucide-react";
import { api } from "@/lib/api";

export const BackendStatus = () => {
  const [status, setStatus] = useState<"loading" | "connected" | "error">("loading");
  const [errorMessage, setErrorMessage] = useState<string>("");

  useEffect(() => {
    checkBackend();
  }, []);

  const checkBackend = async () => {
    try {
      await api.healthCheck();
      setStatus("connected");
    } catch (error) {
      setStatus("error");
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "Cannot connect to backend"
      );
    }
  };

  if (status === "loading") {
    return (
      <Alert className="mb-4">
        <Loader2 className="h-4 w-4 animate-spin" />
        <AlertTitle>Checking backend connection...</AlertTitle>
      </Alert>
    );
  }

  if (status === "error") {
    return (
      <Alert variant="destructive" className="mb-4">
        <XCircle className="h-4 w-4" />
        <AlertTitle>Backend Not Connected</AlertTitle>
        <AlertDescription>
          {errorMessage}
          <br />
          <span className="text-sm">
            Make sure the backend server is running: <code>cd backend && python main.py</code>
          </span>
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <Alert className="mb-4 border-green-500 bg-green-50 dark:bg-green-950">
      <CheckCircle2 className="h-4 w-4 text-green-600" />
      <AlertTitle className="text-green-800 dark:text-green-200">
        Backend Connected
      </AlertTitle>
      <AlertDescription className="text-green-700 dark:text-green-300">
        API is running and ready to use
      </AlertDescription>
    </Alert>
  );
};
