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
  ResponsiveContainer,
  ScatterChart,
  Scatter
} from "recharts";
import DataService from "./DataService";
import moment from "moment";

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
      graphData: [],
      currentCustomerCount: {
        datetime: "",
        count: 0
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
        let data = counts.map((count, index) => ({
          name: index,
          customers: count
        }));
        let maxCount = 0;
        data.forEach(record => {
          maxCount = Math.max(maxCount, record.customers);
        });
        this.state.maxCount = maxCount;
        this.setState(this.state);
      });
    };

    let updateGraphData = () => {
      dataService.currentCustomerCounts().then(count => {
        let countData = {
          time: count.datetime,
          number: count.count
        };
        if (this.state.graphData.length < 1) {
          this.setState(prevState => ({
            graphData: [...prevState.graphData, countData]
          }));
        } else if (
          this.state.graphData[this.state.graphData.length - 1].number !=
          countData.number
        ) {
          this.setState(prevState => ({
            graphData: [...prevState.graphData, countData]
          }));
        }
        console.log(this.state.graphData);
      });
    };

    updateCurrentCustomerCount();

    updateCustomerCounts();

    updateGraphData();

    setInterval(() => {
      updateCurrentCustomerCount();
      updateCustomerCounts();
    }, 1000);

    setInterval(() => {
      updateGraphData();
    }, 5000);
  }

  render() {
    return (
      <div>
        <AppContainer>
          <Columns>
            <Column size="isTwoThirds">
              <ChartTitle> Customers in Store </ChartTitle>
              <ResponsiveContainer width="95%" height={400}>
                <ScatterChart>
                  <XAxis
                    dataKey="time"
                    domain={["auto", "auto"]}
                    name="Time"
                    tickFormatter={unixTime =>
                      moment(unixTime * 1000).format("HH:mm:ss")
                    }
                    type="number"
                  />
                  <YAxis dataKey="number" name="Value" />

                  <Scatter
                    data={this.state.graphData}
                    line={{ stroke: "#333" }}
                    lineJointType="monotoneX"
                    lineType="joint"
                    name="Values"
                  />
                </ScatterChart>
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
