import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
  Paper,
} from '@mui/material';
import {
  Warning,
  CheckCircle,
  Error,
  Info,
} from '@mui/icons-material';
import { dashboard } from '../api/client';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await dashboard.getStats();
      setStats(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Failed to load stats:', err);
      setError('Failed to load dashboard statistics');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        SOC Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Total Alerts */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <div>
                  <Typography color="textSecondary" variant="body2" gutterBottom>
                    Total Alerts
                  </Typography>
                  <Typography variant="h4">{stats?.alerts?.total || 0}</Typography>
                </div>
                <Warning sx={{ fontSize: 48, color: '#757575' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* New Alerts */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <div>
                  <Typography color="textSecondary" variant="body2" gutterBottom>
                    New Alerts
                  </Typography>
                  <Typography variant="h4" color="error">
                    {stats?.alerts?.new || 0}
                  </Typography>
                </div>
                <Error sx={{ fontSize: 48, color: '#f44336' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Critical Alerts */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <div>
                  <Typography color="textSecondary" variant="body2" gutterBottom>
                    Critical Alerts
                  </Typography>
                  <Typography variant="h4" color="warning.main">
                    {stats?.alerts?.critical || 0}
                  </Typography>
                </div>
                <Warning sx={{ fontSize: 48, color: '#ff9800' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Open Incidents */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <div>
                  <Typography color="textSecondary" variant="body2" gutterBottom>
                    Open Incidents
                  </Typography>
                  <Typography variant="h4" color="info.main">
                    {stats?.incidents?.open || 0}
                  </Typography>
                </div>
                <Info sx={{ fontSize: 48, color: '#2196f3' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Alerts by Severity */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Alerts by Severity
            </Typography>
            <Box sx={{ mt: 2 }}>
              {stats?.alerts?.by_severity?.map((item, index) => (
                <Box 
                  key={index}
                  sx={{ 
                    display: 'flex', 
                    justifyContent: 'space-between',
                    mb: 1,
                    p: 1,
                    bgcolor: '#f5f5f5',
                    borderRadius: 1
                  }}
                >
                  <Typography variant="body1">{item.severity}</Typography>
                  <Typography variant="body1" fontWeight="bold">{item.count}</Typography>
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>

        {/* Top MITRE Techniques */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Top MITRE ATT&CK Techniques
            </Typography>
            <Box sx={{ mt: 2 }}>
              {stats?.top_mitre_techniques?.length > 0 ? (
                stats.top_mitre_techniques.map((technique, index) => (
                  <Box 
                    key={index}
                    sx={{ 
                      display: 'flex', 
                      justifyContent: 'space-between',
                      mb: 1,
                      p: 1,
                      bgcolor: '#f5f5f5',
                      borderRadius: 1
                    }}
                  >
                    <Typography variant="body2">{technique.technique_id} - {technique.name}</Typography>
                    <Typography variant="body2" fontWeight="bold" color="primary">
                      {technique.count}
                    </Typography>
                  </Box>
                ))
              ) : (
                <Typography variant="body2" color="textSecondary">No data available</Typography>
              )}
            </Box>
          </Paper>
        </Grid>

        {/* Playbook Statistics */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Playbook Execution Statistics
            </Typography>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} sm={4}>
                <Box textAlign="center">
                  <Typography variant="h3" color="primary">
                    {stats?.playbooks?.total_executions || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Total Executions
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Box textAlign="center">
                  <Typography variant="h3" color="success.main">
                    {stats?.playbooks?.successful || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Successful
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Box textAlign="center">
                  <Typography variant="h3" color="info.main">
                    {stats?.playbooks?.success_rate?.toFixed(1) || 0}%
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Success Rate
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;