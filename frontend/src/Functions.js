import React, { Component } from "react";
import styled from "styled-components";
import { Column, Columns } from "re-bulma";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  Tooltip,
  XAxis,
  YAxis,
  ResponsiveContainer
} from "recharts";
import DataService from "./DataService";

const AppContainer = styled.div`
  padding: 2%;
  max-width: 90%;
  margin: auto;
`;

const Card = styled.div`
  padding-top:
  width: 90%;
  height: 175px;
  background: #fff;
  margin-top: 2%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);

  &:hover {
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.10), 0 5px 5px rgba(0, 0, 0, 0.10);
    cursor: pointer;
  }
`;

const Title = styled.h1`
  text-transform: uppercase;
  letter-spacing: 3px;
  font-size: 1.5rem;
  padding: 2%;
  color: #103fb9;
  text-align: center;
`;

const HeatmapTitle = styled.h1`
  text-transform: uppercase;
  letter-spacing: 3px;
  font-size: 1.5rem;
  color: #103fb9;
  text-align: center;

  &:hover {
    opacity: 0.5;
    transition: all 300ms ease;
  }
`;

const ChartTitle = styled.h1`
  font-size: 1.5rem;
  padding: 2%;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 2px;
  background: #103fb9;
  color: #fff;
`;

const Data = styled.div`
  font-size: ${props => props.sz};
  text-align: center;
  font-weight: 800;
`;
const HeatMap = styled.div`
  width: 100%;
  border: 1px solid #d8dbe4;
`;

class Functions extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      currentCustomerCount: {
        count: 0,
        datetime: ""
      },
      totalCustomerCount: {
        count: 100
      },
      customerPositions: {
        positions: []
      },
      maxCount: 0
    };
    let dataService = new DataService();

    let updateCurrentCustomerCount = () => {
      dataService.currentCustomerCounts().then(count => {
        this.state.currentCustomerCount = count;
        this.setState(this.state);
      });
    };

    let updateCustomerCounts = () => {
      dataService.customerCounts().then(counts => {
        this.state.data = counts.map((count, index) => ({
          name: index,
          customers: count
        }));
        let maxCount = 0;
        this.state.data.forEach(record => {
          maxCount = Math.max(maxCount, record.customers);
        });
        this.state.maxCount = maxCount;
        this.setState(this.state);
      });
    };

    updateCurrentCustomerCount();

    updateCustomerCounts();

    setInterval(() => {
      updateCurrentCustomerCount();
      updateCustomerCounts();
    }, 1000);
  }

  render() {
    return (
      <div>
        <AppContainer>
          <Columns>
            <Column size="isTwoThirds">
              <ChartTitle> Customers in Store </ChartTitle>
              <ResponsiveContainer width="95%" height={400}>
                <LineChart
                  data={this.state.data}
                  margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                  <XAxis dataKey="name" />
                  <YAxis />
                  <CartesianGrid strokeDasharray="3 3" />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="customers"
                    stroke="#3a7bd5"
                    activeDot={{ r: 8 }}
                  />
                </LineChart>
              </ResponsiveContainer>
              <br />
              <br />
              <a href="/heatmap.html">
                <HeatmapTitle>View Heatmap</HeatmapTitle>
              </a>
            </Column>
            <Column>
              <Card>
                <Title>Active Customers</Title>
                <Data sz="3rem">{this.state.currentCustomerCount.count}</Data>
              </Card>
              <Card>
                <Title>Max Number Customers</Title>
                <Data sz="3rem">{this.state.maxCount}</Data>
              </Card>
              <Card>
                <Title>Revenue per Customer</Title>
                <Data sz="3rem">${Math.floor(1000 / this.state.maxCount)}</Data>
                <Data sz="1em">$1000/{this.state.maxCount}</Data>
              </Card>
            </Column>
          </Columns>
        </AppContainer>
      </div>
    );
  }
}

export default Functions;
