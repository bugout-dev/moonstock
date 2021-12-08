import { useMutation, useQuery } from "react-query";
import { useRouter, useToast } from ".";
import { queryCacheProps } from "./hookCommon";
import { DashboardService } from "../services";
import { useContext } from "react";
import UserContext from "../providers/UserProvider/context";
import {
  uniqueNamesGenerator,
  adjectives,
  colors,
  starWars,
} from "unique-names-generator";

const useDashboard = (dashboardId) => {
  const toast = useToast();
  const router = useRouter();
  const { user } = useContext(UserContext);

  const dashboardsListCache = useQuery(
    ["dashboards-list"],
    DashboardService.getDashboardsList,
    {
      ...queryCacheProps,
      onError: (error) => {
        toast(error, "error");
      },
      enabled: !!user,
    }
  );

  const _createDashboard = async (dashboard) => {
    const _dashboard = { ...dashboard };
    console.log("dashboard", _dashboard);
    if (!_dashboard.name || _dashboard.name === "")
      _dashboard.name = uniqueNamesGenerator({
        dictionaries: [colors, adjectives, starWars],
      });
    if (!_dashboard.subscription_settings) {
      _dashboard.subscription_settings = [];
    }
    DashboardService.createDashboard(_dashboard);
  };

  const createDashboard = useMutation(_createDashboard, {
    onSuccess: () => {
      toast("Created new dashboard", "success");
      sessionStorage.removeItem("new_dashboard");
    },
    onError: (error) => {
      toast(error.error, "error", "Fail");
    },
    onSettled: () => {
      dashboardsListCache.refetch();
    },
  });

  const updateDashboard = useMutation(DashboardService.updateDashboard, {
    onSuccess: () => {
      toast("Updated new dashboard", "success");
    },
    onError: (error) => {
      toast(error.error, "error", "Fail");
    },
    onSettled: () => {
      dashboardsListCache.refetch();
    },
  });

  const deleteDashboard = useMutation(
    () => DashboardService.deleteDashboard(dashboardId),
    {
      onSuccess: () => {
        toast("Deleted dashboard", "success");
        router.push("/welcome");
      },
      onError: (error) => {
        toast(error.error, "error", "Fail");
      },
      onSettled: () => {
        dashboardsListCache.refetch();
      },
    }
  );

  const dashboardCache = useQuery(
    ["dashboards", { dashboardId }],
    () => DashboardService.getDashboard(dashboardId),
    {
      ...queryCacheProps,
      onError: (error) => {
        toast(error, "error");
      },
      enabled: !!user && !!dashboardId,
    }
  );

  const dashboardLinksCache = useQuery(
    ["dashboardLinks", { dashboardId }],
    () => DashboardService.getDashboardLinks(dashboardId),
    {
      ...queryCacheProps,
      onError: (error) => {
        toast(error, "error");
      },
      enabled: !!user && !!dashboardId,
    }
  );

  return {
    createDashboard,
    dashboardsListCache,
    dashboardCache,
    deleteDashboard,
    dashboardLinksCache,
    updateDashboard,
  };
};

export default useDashboard;
