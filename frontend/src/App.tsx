import {
  ArrowDown,
  ArrowRight,
  BrainCircuit,
  ChevronDown,
  CircleAlert,
  Database,
  Gauge,
  ShieldCheck,
  Sparkles,
  TrendingDown,
  TrendingUp,
} from 'lucide-react'

import {
  useEffect,
  useMemo,
  useState,
} from 'react'

import type {
  FormEvent,
} from 'react'
import './App.css'
import MotionField from './MotionField'

type CustomerForm = {
  gender: string
  SeniorCitizen: number
  Partner: string
  Dependents: string
  tenure: number
  PhoneService: string
  MultipleLines: string
  InternetService: string
  OnlineSecurity: string
  OnlineBackup: string
  DeviceProtection: string
  TechSupport: string
  StreamingTV: string
  StreamingMovies: string
  Contract: string
  PaperlessBilling: string
  PaymentMethod: string
  MonthlyCharges: number
  TotalCharges: number
  ServiceCount: number
  AverageMonthlySpend: number
}

type LocalExplanation = {
  feature: string
  shap_value: number
  impact: string
  absolute_impact: number
}

type GlobalDriver = {
  feature: string
  importance: number
}

type PredictionResult = {
  churn_probability: number
  prediction: number
  risk_level: string
  local_explanation: LocalExplanation[]
  global_drivers: GlobalDriver[]
}

const API_URL = '/api'

const initialCustomer: CustomerForm = {
  gender: 'Female',
  SeniorCitizen: 0,
  Partner: 'No',
  Dependents: 'No',
  tenure: 5,
  PhoneService: 'Yes',
  MultipleLines: 'No',
  InternetService: 'DSL',
  OnlineSecurity: 'No',
  OnlineBackup: 'No',
  DeviceProtection: 'No',
  TechSupport: 'No',
  StreamingTV: 'No',
  StreamingMovies: 'No',
  Contract: 'Month-to-month',
  PaperlessBilling: 'Yes',
  PaymentMethod: 'Credit card (automatic)',
  MonthlyCharges: 44.05,
  TotalCharges: 202.15,
  ServiceCount: 0,
  AverageMonthlySpend: 40.43,
}

const OPTIONS = {
  gender: ['Female', 'Male'],
  binary: ['No', 'Yes'],
  multipleLines: ['No phone service', 'No', 'Yes'],
  internet: ['DSL', 'Fiber optic', 'No'],
  internetFeature: ['No internet service', 'No', 'Yes'],
  contract: ['Month-to-month', 'One year', 'Two year'],
  payment: [
    'Electronic check',
    'Mailed check',
    'Bank transfer (automatic)',
    'Credit card (automatic)',
  ],
}

function App() {
  const [customer, setCustomer] =
      useState<CustomerForm>(initialCustomer)

  const [result, setResult] =
      useState<PredictionResult | null>(null)

  const [loading, setLoading] = useState(false)

  const [apiError, setApiError] =
      useState('')

  const [scrollProgress, setScrollProgress] =
      useState(0)

  useEffect(() => {
    const handleScroll = () => {
      const max =
          document.documentElement.scrollHeight -
          window.innerHeight

      setScrollProgress(
          max > 0
              ? Math.min(
                  1,
                  Math.max(0, window.scrollY / max),
              )
              : 0,
      )
    }

    handleScroll()

    window.addEventListener(
        'scroll',
        handleScroll,
        { passive: true },
    )

    window.addEventListener(
        'resize',
        handleScroll,
    )

    return () => {
      window.removeEventListener(
          'scroll',
          handleScroll,
      )

      window.removeEventListener(
          'resize',
          handleScroll,
      )
    }
  }, [])

  const updateField = <
      K extends keyof CustomerForm,
  >(
      field: K,
      value: CustomerForm[K],
  ) => {
    setCustomer((current) => ({
      ...current,
      [field]: value,
    }))
  }

  const analyzeCustomer = async (
      event?: FormEvent,
  ) => {
    event?.preventDefault()

    setLoading(true)
    setApiError('')

    try {
      const response = await fetch(
          `${API_URL}/predict`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(customer),
          },
      )

      if (!response.ok) {
        const errorText =
            await response.text()

        throw new Error(
            errorText ||
            `API request failed: ${response.status}`,
        )
      }

      const data = await response.json()

      setResult(data.result)

      window.setTimeout(() => {
        document
            .getElementById('analysis')
            ?.scrollIntoView({
              behavior: 'smooth',
              block: 'start',
            })
      }, 80)
    } catch (error) {
      console.error(error)

      setApiError(
          'KINETICS could not complete the inference request. Please try again.',
      )
    } finally {
      setLoading(false)
    }
  }

  const probability =
      result?.churn_probability ?? 0

  const probabilityPercent =
      probability * 100

  const riskClass =
      result?.risk_level.toLowerCase() ?? 'idle'

  const topRiskDrivers = useMemo(
      () =>
          result?.local_explanation.filter(
              (item) => item.shap_value > 0,
          ) ?? [],
      [result],
  )

  const protectiveDrivers = useMemo(
      () =>
          result?.local_explanation.filter(
              (item) => item.shap_value < 0,
          ) ?? [],
      [result],
  )

  return (
      <div className="kinetics-app">
        <MotionField />
        <div
            className="scroll-meter"
            style={{
              transform: `scaleX(${scrollProgress})`,
            }}
        />

        <div className="ambient ambient-one" />
        <div className="ambient ambient-two" />
        <div className="grain" />

        <header className="site-header">
          <a
              className="brand"
              href="#top"
              aria-label="KINETICS home"
          >
          <span className="brand-symbol">
            ✳
          </span>

            <span>
            <strong>KINETICS</strong>
            <small>
              Customer intelligence
            </small>
          </span>
          </a>

          <nav className="site-nav">
            <a href="#intelligence">
              Intelligence
            </a>

            <a href="#behavior">
              Behavior
            </a>

            <a href="#model">
              Model
            </a>

            <a
                href={result ? "#retention" : "#analyzer"}
                onClick={() => {
                  if (!result) {
                    setTimeout(() => {
                      document
                          .getElementById("analyzer")
                          ?.scrollIntoView({
                            behavior: "smooth",
                            block: "start",
                          });
                    }, 0);
                  }
                }}
            >
              Retention
            </a>

            <a
                className="nav-pill"
                href="#analyzer"
            >
              Analyze customer
            </a>
          </nav>
        </header>

        <main id="top">
          <section className="hero-stage">
            <div className="hero-orbit orbit-one" />
            <div className="hero-orbit orbit-two" />

            <div className="hero-content">
              <div className="eyebrow">
                <span>Customer intelligence</span>
                <i>·</i>
                <span>Machine learning</span>
              </div>

              <h1>
                Customer behavior,
                <br />
                <em>made visible.</em>
              </h1>

              <p className="hero-copy">
                KINETICS turns customer attributes into
                explainable churn intelligence, combining
                predictive modeling with transparent model
                reasoning.
              </p>

              <div className="hero-actions">
                <a
                    className="dark-pill"
                    href="#analyzer"
                >
                  Start an analysis
                  <ArrowRight size={16} />
                </a>

                <a
                    className="text-link"
                    href="#intelligence"
                >
                  Explore the model
                  <ArrowDown size={15} />
                </a>
              </div>
            </div>

            <div className="hero-status">
              <span className="status-dot" />
              Inference engine ready
            </div>
          </section>

          <section
              id="intelligence"
              className="story-stage"
          >
            <div className="story-copy">
              <div className="eyebrow">
                <span>01</span>
                <i>·</i>
                <span>Understand</span>
              </div>

              <h2>
                Churn is not
                <br />
                <em>just a number.</em>
              </h2>

              <p>
                KINETICS examines behavioral and account
                characteristics to identify patterns
                associated with customer churn.
              </p>
            </div>

            <div className="intelligence-card">
              <div className="card-label">
                Model intelligence
              </div>

              <div className="metric-large">
                0.868
              </div>

              <div className="metric-caption">
                ROC-AUC
              </div>

              <div className="metric-grid">
                <Metric
                    label="PR-AUC"
                    value="0.711"
                />

                <Metric
                    label="F1"
                    value="0.638"
                />

                <Metric
                    label="Precision"
                    value="0.721"
                />

                <Metric
                    label="Recall"
                    value="0.571"
                />
              </div>

              <div className="card-foot">
                <BrainCircuit size={15} />
                Tuned Gradient Boosting
              </div>
            </div>
          </section>

          <section
              id="behavior"
              className="behavior-stage"
          >
            <div className="behavior-header">
              <div>
                <div className="eyebrow">
                  <span>01.5</span>
                  <i>·</i>
                  <span>Customer behavior</span>
                </div>

                <h2>
                  The data
                  <br />
                  <em>has a pattern.</em>
                </h2>
              </div>

              <p>
                Before prediction, KINETICS examines the
                cleaned customer population to understand
                where churn appears most frequently.
              </p>
            </div>

            <div className="behavior-overview">
              <div className="behavior-stat primary">
                <span>Overall churn rate</span>

                <strong>26.49%</strong>

                <small>
                  1,857 of 7,010 customers
                </small>
              </div>

              <div className="behavior-stat">
                <span>Stayed</span>

                <strong>73.51%</strong>

                <small>
                  5,153 customers
                </small>
              </div>

              <div className="behavior-stat">
                <span>Dataset</span>

                <strong>7,010</strong>

                <small>
                  cleaned customer records
                </small>
              </div>
            </div>

            <div className="behavior-grid">
              <BehaviorCard
                  eyebrow="Contract"
                  title="Commitment changes the picture."
                  description="Churn is substantially higher among month-to-month customers in the observed dataset."
              >
                <BehaviorBar
                    label="Month-to-month"
                    value={42.64}
                    display="42.64%"
                />

                <BehaviorBar
                    label="One year"
                    value={11.28}
                    display="11.28%"
                />

                <BehaviorBar
                    label="Two year"
                    value={2.85}
                    display="2.85%"
                />
              </BehaviorCard>

              <BehaviorCard
                  eyebrow="Internet service"
                  title="Service type separates behavior."
                  description="Fiber-optic customers show a higher observed churn rate than DSL or customers without internet service."
              >
                <BehaviorBar
                    label="Fiber optic"
                    value={41.78}
                    display="41.78%"
                />

                <BehaviorBar
                    label="DSL"
                    value={18.93}
                    display="18.93%"
                />

                <BehaviorBar
                    label="No internet"
                    value={7.24}
                    display="7.24%"
                />
              </BehaviorCard>

              <BehaviorCard
                  eyebrow="Payment method"
                  title="Payment behavior is another signal."
                  description="Electronic-check customers have the highest observed churn rate among the payment groups."
              >
                <BehaviorBar
                    label="Electronic check"
                    value={45.15}
                    display="45.15%"
                />

                <BehaviorBar
                    label="Mailed check"
                    value={19.02}
                    display="19.02%"
                />

                <BehaviorBar
                    label="Bank transfer"
                    value={16.73}
                    display="16.73%"
                />

                <BehaviorBar
                    label="Credit card"
                    value={15.25}
                    display="15.25%"
                />
              </BehaviorCard>

              <BehaviorCard
                  eyebrow="Customer tenure"
                  title="Churned customers are newer."
                  description="The average observed tenure differs substantially between the two groups."
              >
                <div className="comparison-stat">
                  <div>
                    <span>Stayed</span>
                    <strong>37.72</strong>
                    <small>months</small>
                  </div>

                  <div>
                    <span>Churned</span>
                    <strong>18.09</strong>
                    <small>months</small>
                  </div>
                </div>

                <div className="comparison-line">
                <span
                    style={{
                      width: `${(18.09 / 37.72) * 100}%`,
                    }}
                />
                </div>
              </BehaviorCard>

              <BehaviorCard
                  eyebrow="Monthly charges"
                  title="Churned customers pay more monthly."
                  description="Average monthly charges are higher in the observed churned group."
              >
                <div className="comparison-stat">
                  <div>
                    <span>Stayed</span>
                    <strong>$61.39</strong>
                    <small>average / month</small>
                  </div>

                  <div>
                    <span>Churned</span>
                    <strong>$74.60</strong>
                    <small>average / month</small>
                  </div>
                </div>

                <div className="charge-difference">
                  <span>Observed difference</span>
                  <strong>+$13.21</strong>
                </div>
              </BehaviorCard>

              <div className="behavior-method">
                <Database size={16} />

                <div>
                  <strong>How to read this</strong>

                  <p>
                    These are descriptive patterns in the
                    cleaned dataset. They show association,
                    not causation, and they should not be
                    interpreted as proof that a particular
                    customer attribute causes churn.
                  </p>
                </div>
              </div>
            </div>
          </section>

          <section
              id="analysis"
              className="prediction-stage"
          >
            <div className="prediction-inner">
              <div className="eyebrow">
                <span>02</span>
                <i>·</i>
                <span>Predict</span>
              </div>

              {!result ? (
                  <div className="empty-analysis">
                    <div className="empty-icon">
                      <Gauge size={24} />
                    </div>

                    <h2>
                      Run an analysis
                    </h2>

                    <p>
                      Submit a customer profile below to
                      generate a real-time churn prediction
                      from the trained KINETICS model.
                    </p>

                    <a
                        className="dark-pill"
                        href="#analyzer"
                    >
                      Open analyzer
                      <ArrowRight size={16} />
                    </a>
                  </div>
              ) : (
                  <div className="result-layout">
                    <div className="risk-card">
                      <div className="card-label">
                        Estimated churn probability
                      </div>

                      <div className="risk-number">
                        {probabilityPercent.toFixed(1)}
                        <span>%</span>
                      </div>

                      <div
                          className={`risk-badge ${riskClass}`}
                      >
                        <span className="status-dot" />
                        {result.risk_level} RISK
                      </div>

                      <div className="risk-result">
                    <span>
                      Model prediction
                    </span>

                        <strong>
                          {result.prediction === 1
                              ? 'CHURN'
                              : 'STAY'}
                        </strong>
                      </div>
                    </div>

                    <div className="prediction-note">
                      <Sparkles size={18} />

                      <div>
                        <strong>
                          Explainable prediction
                        </strong>

                        <p>
                          The probability comes directly
                          from the trained Gradient Boosting
                          pipeline. The factors below show
                          how the model arrived at this
                          individual prediction.
                        </p>
                      </div>
                    </div>
                  </div>
              )}
            </div>
          </section>

          {result && (
              <section className="explanation-stage">
                <div className="explanation-header">
                  <div>
                    <div className="eyebrow">
                      <span>03</span>
                      <i>·</i>
                      <span>Explain</span>
                    </div>

                    <h2>
                      Why this
                      <br />
                      <em>prediction?</em>
                    </h2>
                  </div>

                  <p>
                    Local SHAP explanations show which
                    observed customer attributes pushed this
                    individual prediction toward or away from
                    churn.
                  </p>
                </div>

                <div className="explanation-grid">
                  <ExplanationColumn
                      title="Increasing churn pressure"
                      icon={<TrendingUp size={17} />}
                      items={topRiskDrivers}
                      positive
                  />

                  <ExplanationColumn
                      title="Reducing churn pressure"
                      icon={<TrendingDown size={17} />}
                      items={protectiveDrivers}
                  />
                </div>

                <div className="method-note">
                  <ShieldCheck size={15} />
                  SHAP values describe model contribution,
                  not causal effects.
                </div>
              </section>
          )}

          {result && (
              <section className="drivers-stage">
                <div className="drivers-heading">
                  <div>
                    <div className="eyebrow">
                      <span>04</span>
                      <i>·</i>
                      <span>Population view</span>
                    </div>

                    <h2>
                      What the model
                      <br />
                      <em>looks for.</em>
                    </h2>
                  </div>

                  <p>
                    Global permutation importance shows which
                    features matter most to predictive
                    performance across the evaluation data.
                  </p>
                </div>

                <div className="drivers-list">
                  {result.global_drivers.map(
                      (driver, index) => (
                          <div
                              className="driver-row"
                              key={driver.feature}
                          >
                    <span className="driver-rank">
                      {String(index + 1).padStart(
                          2,
                          '0',
                      )}
                    </span>

                            <span className="driver-name">
                      {driver.feature}
                    </span>

                            <div className="driver-bar">
                      <span
                          style={{
                            width: `${Math.min(
                                100,
                                (driver.importance /
                                    result.global_drivers[0]
                                        .importance) *
                                100,
                            )}%`,
                          }}
                      />
                            </div>

                            <span className="driver-value">
                      {driver.importance.toFixed(
                          4,
                      )}
                    </span>
                          </div>
                      ),
                  )}
                </div>
              </section>
          )}

          <section
              id="model"
              className="model-stage"
          >
            <div className="model-header">
              <div>
                <div className="eyebrow">
                  <span>04.5</span>
                  <i>·</i>
                  <span>Model evaluation</span>
                </div>

                <h2>
                  Measure what
                  <br />
                  <em>the model gets right.</em>
                </h2>
              </div>

              <p>
                KINETICS evaluates multiple classification
                models on a held-out test set. No single
                metric tells the complete story.
              </p>
            </div>

            <div className="evaluation-banner">
              <div>
                <span>Selected inference model</span>

                <strong>
                  Gradient Boosting
                </strong>

                <small>
                  Tuned with stratified 5-fold
                  cross-validation
                </small>
              </div>

              <div className="evaluation-status">
                <CheckCircleIcon />
                <span>
                Inference ready
              </span>
              </div>
            </div>

            <div className="model-comparison">
              <ModelCard
                  name="Gradient Boosting"
                  tag="Tuned"
                  metrics={[
                    ['F1 score', '0.638'],
                    ['ROC-AUC', '0.868'],
                    ['PR-AUC', '0.711'],
                    ['Precision', '0.721'],
                    ['Recall', '0.571'],
                  ]}
                  featured
              />

              <ModelCard
                  name="Logistic Regression"
                  tag="Tuned"
                  metrics={[
                    ['F1 score', '0.624'],
                    ['ROC-AUC', '0.850'],
                    ['PR-AUC', '0.647'],
                    ['Precision', '0.516'],
                    ['Recall', '0.790'],
                  ]}
              />
            </div>

            <div className="metric-explanation">
              <div className="metric-explanation-item">
              <span className="metric-symbol">
                F1
              </span>

                <div>
                  <strong>
                    Balance between precision and recall
                  </strong>

                  <p>
                    Useful when both missed churners and
                    unnecessary interventions matter.
                  </p>
                </div>
              </div>

              <div className="metric-explanation-item">
              <span className="metric-symbol">
                ROC
              </span>

                <div>
                  <strong>
                    Ranking ability across thresholds
                  </strong>

                  <p>
                    Measures how well the model separates
                    churned and retained customers.
                  </p>
                </div>
              </div>

              <div className="metric-explanation-item">
              <span className="metric-symbol">
                PR
              </span>

                <div>
                  <strong>
                    Precision-recall performance
                  </strong>

                  <p>
                    Particularly informative when the
                    positive class is less common.
                  </p>
                </div>
              </div>
            </div>

            <div className="model-tradeoff">
              <div className="tradeoff-icon">
                ↔
              </div>

              <div>
                <strong>
                  Different objectives produce different
                  behavior.
                </strong>

                <p>
                  Logistic Regression reaches higher recall
                  on the held-out test set, while Gradient
                  Boosting reaches higher precision, F1,
                  ROC-AUC and PR-AUC. The appropriate
                  operating point depends on the cost of
                  missed churn versus unnecessary retention
                  actions.
                </p>
              </div>
            </div>

            <div className="model-method">
              <Database size={15} />

              <span>
              Evaluation uses a stratified held-out test
              set of 1,402 customers.
            </span>
            </div>
          </section>

          {result && (
              <section id="retention" className="retention-stage">
                <div className="retention-header">
                  <div>
                    <div className="eyebrow">
                      <span>04.8</span>
                      <i>·</i>
                      <span>Retention intelligence</span>
                    </div>

                    <h2>
                      From prediction
                      <br />
                      <em>to action.</em>
                    </h2>
                  </div>

                  <p>
                    The model identifies a risk signal. This
                    layer translates that signal into a
                    practical review workflow without treating
                    model associations as causal explanations.
                  </p>
                </div>

                <div className="retention-summary">
                  <div
                      className={`retention-risk ${riskClass}`}
                  >
                    <span>Current model signal</span>

                    <strong>
                      {result.risk_level}
                    </strong>

                    <small>
                      {probabilityPercent.toFixed(1)}%
                      estimated churn probability
                    </small>
                  </div>

                  <div className="retention-summary-copy">
                    <div className="retention-summary-icon">
                      <Sparkles size={18} />
                    </div>

                    <div>
                      <strong>
                        {result.prediction === 1
                            ? 'Prioritize human review'
                            : 'Continue standard engagement'}
                      </strong>

                      <p>
                        {result.prediction === 1
                            ? 'The model currently classifies this customer as higher risk. Review the strongest contributing signals before deciding on any retention action.'
                            : 'The model does not currently classify this customer as likely to churn. Continue normal engagement while monitoring future customer behavior.'}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="retention-grid">
                  <RetentionCard
                      number="01"
                      title="Review the strongest signals"
                  >
                    <p>
                      Start with the features that contributed
                      most strongly to this individual
                      prediction.
                    </p>

                    <div className="retention-feature-list">
                      {topRiskDrivers
                          .slice(0, 3)
                          .map((driver) => (
                              <div
                                  className="retention-feature"
                                  key={driver.feature}
                              >
                        <span>
                          {formatFeatureName(
                              driver.feature,
                          )}
                        </span>

                                <strong>
                                  +{driver.shap_value.toFixed(
                                    3,
                                )}
                                </strong>
                              </div>
                          ))}
                    </div>
                  </RetentionCard>

                  <RetentionCard
                      number="02"
                      title="Understand the customer context"
                  >
                    <p>
                      A model score should be considered
                      alongside the customer's actual account
                      context and recent interactions.
                    </p>

                    <div className="context-list">
                      <ContextRow
                          label="Contract"
                          value={customer.Contract}
                      />

                      <ContextRow
                          label="Tenure"
                          value={`${customer.tenure} months`}
                      />

                      <ContextRow
                          label="Monthly charges"
                          value={`$${customer.MonthlyCharges.toFixed(
                              2,
                          )}`}
                      />
                    </div>
                  </RetentionCard>

                  <RetentionCard
                      number="03"
                      title="Choose an appropriate response"
                  >
                    <p>
                      KINETICS does not prescribe an automatic
                      intervention. The prediction is a signal
                      for informed human review.
                    </p>

                    <div className="response-list">
                      <ResponseItem
                          icon={<CircleAlert size={15} />}
                          text="Review account history"
                      />

                      <ResponseItem
                          icon={<ShieldCheck size={15} />}
                          text="Check current service experience"
                      />

                      <ResponseItem
                          icon={<ArrowRight size={15} />}
                          text="Decide whether outreach is warranted"
                      />
                    </div>
                  </RetentionCard>
                </div>

                <div className="retention-disclaimer">
                  <ShieldCheck size={15} />

                  <span>
                KINETICS provides decision support, not
                automatic retention decisions. Model
                outputs should be reviewed with current
                customer context.
              </span>
                </div>
              </section>
          )}

          <section
              id="analyzer"
              className="analyzer-stage"
          >
            <div className="analyzer-heading">
              <div className="eyebrow">
                <span>05</span>
                <i>·</i>
                <span>Customer analyzer</span>
              </div>

              <h2>
                Put a customer
                <br />
                <em>under the lens.</em>
              </h2>

              <p>
                Enter observed customer attributes. KINETICS
                sends the profile directly to the FastAPI
                inference engine.
              </p>
            </div>

            <form
                className="analyzer-card"
                onSubmit={analyzeCustomer}
            >
              <FormSection
                  title="Customer profile"
                  icon={<ShieldCheck size={17} />}
              >
                <SelectField
                    label="Gender"
                    value={customer.gender}
                    options={OPTIONS.gender}
                    onChange={(value) =>
                        updateField('gender', value)
                    }
                />

                <SelectField
                    label="Senior citizen"
                    value={String(
                        customer.SeniorCitizen,
                    )}
                    options={['0', '1']}
                    onChange={(value) =>
                        updateField(
                            'SeniorCitizen',
                            Number(value),
                        )
                    }
                />

                <SelectField
                    label="Partner"
                    value={customer.Partner}
                    options={OPTIONS.binary}
                    onChange={(value) =>
                        updateField(
                            'Partner',
                            value,
                        )
                    }
                />

                <SelectField
                    label="Dependents"
                    value={customer.Dependents}
                    options={OPTIONS.binary}
                    onChange={(value) =>
                        updateField(
                            'Dependents',
                            value,
                        )
                    }
                />

                <NumberField
                    label="Tenure (months)"
                    value={customer.tenure}
                    onChange={(value) =>
                        updateField(
                            'tenure',
                            value,
                        )
                    }
                />

                <SelectField
                    label="Phone service"
                    value={customer.PhoneService}
                    options={OPTIONS.binary}
                    onChange={(value) =>
                        updateField(
                            'PhoneService',
                            value,
                        )
                    }
                />
              </FormSection>

              <FormSection
                  title="Services"
                  icon={<Database size={17} />}
              >
                <SelectField
                    label="Multiple lines"
                    value={customer.MultipleLines}
                    options={
                      OPTIONS.multipleLines
                    }
                    onChange={(value) =>
                        updateField(
                            'MultipleLines',
                            value,
                        )
                    }
                />

                <SelectField
                    label="Internet service"
                    value={
                      customer.InternetService
                    }
                    options={OPTIONS.internet}
                    onChange={(value) =>
                        updateField(
                            'InternetService',
                            value,
                        )
                    }
                />

                <SelectField
                    label="Online security"
                    value={
                      customer.OnlineSecurity
                    }
                    options={
                      OPTIONS.internetFeature
                    }
                    onChange={(value) =>
                        updateField(
                            'OnlineSecurity',
                            value,
                        )
                    }
                />

                <SelectField
                    label="Online backup"
                    value={
                      customer.OnlineBackup
                    }
                    options={
                      OPTIONS.internetFeature
                    }
                    onChange={(value) =>
                        updateField(
                            'OnlineBackup',
                            value,
                        )
                    }
                />

                <SelectField
                    label="Device protection"
                    value={
                      customer.DeviceProtection
                    }
                    options={
                      OPTIONS.internetFeature
                    }
                    onChange={(value) =>
                        updateField(
                            'DeviceProtection',
                            value,
                        )
                    }
                />

                <SelectField
                    label="Tech support"
                    value={
                      customer.TechSupport
                    }
                    options={
                      OPTIONS.internetFeature
                    }
                    onChange={(value) =>
                        updateField(
                            'TechSupport',
                            value,
                        )
                    }
                />

                <SelectField
                    label="Streaming TV"
                    value={customer.StreamingTV}
                    options={
                      OPTIONS.internetFeature
                    }
                    onChange={(value) =>
                        updateField(
                            'StreamingTV',
                            value,
                        )
                    }
                />

                <SelectField
                    label="Streaming movies"
                    value={
                      customer.StreamingMovies
                    }
                    options={
                      OPTIONS.internetFeature
                    }
                    onChange={(value) =>
                        updateField(
                            'StreamingMovies',
                            value,
                        )
                    }
                />
              </FormSection>

              <FormSection
                  title="Billing & contract"
                  icon={<Gauge size={17} />}
              >
                <SelectField
                    label="Contract"
                    value={customer.Contract}
                    options={OPTIONS.contract}
                    onChange={(value) =>
                        updateField(
                            'Contract',
                            value,
                        )
                    }
                />

                <SelectField
                    label="Paperless billing"
                    value={
                      customer.PaperlessBilling
                    }
                    options={OPTIONS.binary}
                    onChange={(value) =>
                        updateField(
                            'PaperlessBilling',
                            value,
                        )
                    }
                />

                <SelectField
                    label="Payment method"
                    value={
                      customer.PaymentMethod
                    }
                    options={OPTIONS.payment}
                    onChange={(value) =>
                        updateField(
                            'PaymentMethod',
                            value,
                        )
                    }
                />

                <NumberField
                    label="Monthly charges"
                    value={
                      customer.MonthlyCharges
                    }
                    step={0.01}
                    onChange={(value) =>
                        updateField(
                            'MonthlyCharges',
                            value,
                        )
                    }
                />

                <NumberField
                    label="Total charges"
                    value={
                      customer.TotalCharges
                    }
                    step={0.01}
                    onChange={(value) =>
                        updateField(
                            'TotalCharges',
                            value,
                        )
                    }
                />

                <NumberField
                    label="Service count"
                    value={
                      customer.ServiceCount
                    }
                    onChange={(value) =>
                        updateField(
                            'ServiceCount',
                            value,
                        )
                    }
                />

                <NumberField
                    label="Average monthly spend"
                    value={
                      customer.AverageMonthlySpend
                    }
                    step={0.01}
                    onChange={(value) =>
                        updateField(
                            'AverageMonthlySpend',
                            value,
                        )
                    }
                />
              </FormSection>

              {apiError && (
                  <div className="api-error">
                    <CircleAlert size={17} />
                    <span>{apiError}</span>
                  </div>
              )}

              <button
                  className="analyze-button"
                  type="submit"
                  disabled={loading}
              >
                {loading ? (
                    <>
                      <span className="spinner" />
                      Running inference...
                    </>
                ) : (
                    <>
                      Analyze churn risk
                      <ArrowRight size={17} />
                    </>
                )}
              </button>

              <p className="form-footnote">
                Analysis uses the trained KINETICS Gradient
                Boosting model and SHAP-based explanations.
              </p>
            </form>
          </section>

          <section className="closing-stage">
            <div className="closing-mark">
              ✳
            </div>

            <h2>
              Understand.
              <br />
              Predict.
              <br />
              <em>Explain.</em>
            </h2>

            <p>
              KINETICS makes machine learning readable enough
              to support the people who actually use its
              predictions.
            </p>

            <a
                className="dark-pill"
                href="#analyzer"
            >
              Analyze another customer
              <ArrowRight size={16} />
            </a>
          </section>
        </main>

        <footer className="site-footer">
        <span>
          KINETICS · Customer Behavior & Churn
          Intelligence
        </span>

          <span>
          Explainable machine learning
        </span>
        </footer>
      </div>
  )
}

function FormSection({
                       title,
                       icon,
                       children,
                     }: {
  title: string
  icon: React.ReactNode
  children: React.ReactNode
}) {
  return (
      <section className="form-section">
        <div className="form-section-header">
        <span className="form-section-icon">
          {icon}
        </span>

          <h3>{title}</h3>
        </div>

        <div className="form-grid">
          {children}
        </div>
      </section>
  )
}

function SelectField({
                       label,
                       value,
                       options,
                       onChange,
                     }: {
  label: string
  value: string
  options: string[]
  onChange: (value: string) => void
}) {
  return (
      <label className="field">
        <span>{label}</span>

        <div className="select-wrap">
          <select
              value={value}
              onChange={(event) =>
                  onChange(event.target.value)
              }
          >
            {options.map((option) => (
                <option
                    value={option}
                    key={option}
                >
                  {option}
                </option>
            ))}
          </select>

          <ChevronDown
              size={15}
              aria-hidden="true"
          />
        </div>
      </label>
  )
}

function NumberField({
                       label,
                       value,
                       onChange,
                       step = 1,
                     }: {
  label: string
  value: number
  onChange: (value: number) => void
  step?: number
}) {
  return (
      <label className="field">
        <span>{label}</span>

        <input
            type="number"
            min="0"
            step={step}
            value={value}
            onChange={(event) =>
                onChange(
                    Number(event.target.value),
                )
            }
        />
      </label>
  )
}

function Metric({
                  label,
                  value,
                }: {
  label: string
  value: string
}) {
  return (
      <div className="mini-metric">
        <strong>{value}</strong>
        <span>{label}</span>
      </div>
  )
}

function ModelCard({
                     name,
                     tag,
                     metrics,
                     featured = false,
                   }: {
  name: string
  tag: string
  metrics: [string, string][]
  featured?: boolean
}) {
  return (
      <article
          className={`model-card ${
              featured ? 'featured' : ''
          }`}
      >
        <div className="model-card-top">
          <div>
          <span className="model-tag">
            {tag}
          </span>

            <h3>{name}</h3>
          </div>

          {featured && (
              <span className="model-selected">
            Active
          </span>
          )}
        </div>

        <div className="model-metrics">
          {metrics.map(([label, value]) => (
              <div
                  className="model-metric"
                  key={label}
              >
                <span>{label}</span>
                <strong>{value}</strong>
              </div>
          ))}
        </div>
      </article>
  )
}

function CheckCircleIcon() {
  return (
      <span className="check-circle-icon">
      ✓
    </span>
  )
}

function formatFeatureName(feature: string) {
  const names: Record<string, string> = {
    Contract: 'Contract',
    tenure: 'Tenure',
    InternetService: 'Internet service',
    MonthlyCharges: 'Monthly charges',
    OnlineSecurity: 'Online security',
    TechSupport: 'Tech support',
    PaymentMethod: 'Payment method',
    AverageMonthlySpend: 'Average monthly spend',
    PaperlessBilling: 'Paperless billing',
    TotalCharges: 'Total charges',
    MultipleLines: 'Multiple lines',
    OnlineBackup: 'Online backup',
    DeviceProtection: 'Device protection',
    SeniorCitizen: 'Senior citizen',
    Dependents: 'Dependents',
    StreamingTV: 'Streaming TV',
    StreamingMovies: 'Streaming movies',
    Partner: 'Partner',
    gender: 'Gender',
    PhoneService: 'Phone service',
  }

  return names[feature] ?? feature
}

function BehaviorCard({
                        eyebrow,
                        title,
                        description,
                        children,
                      }: {
  eyebrow: string
  title: string
  description: string
  children: React.ReactNode
}) {
  return (
      <article className="behavior-card">
        <div className="behavior-card-eyebrow">
          {eyebrow}
        </div>

        <h3>{title}</h3>

        <p>{description}</p>

        <div className="behavior-card-content">
          {children}
        </div>
      </article>
  )
}

function BehaviorBar({
                       label,
                       value,
                       display,
                     }: {
  label: string
  value: number
  display: string
}) {
  return (
      <div className="behavior-bar">
        <div className="behavior-bar-label">
          <span>{label}</span>
          <strong>{display}</strong>
        </div>

        <div className="behavior-bar-track">
        <span
            style={{
              width: `${value}%`,
            }}
        />
        </div>
      </div>
  )
}

function RetentionCard({
                         number,
                         title,
                         children,
                       }: {
  number: string
  title: string
  children: React.ReactNode
}) {
  return (
      <article className="retention-card">
        <div className="retention-card-number">
          {number}
        </div>

        <h3>{title}</h3>

        {children}
      </article>
  )
}

function ContextRow({
                      label,
                      value,
                    }: {
  label: string
  value: string
}) {
  return (
      <div className="context-row">
        <span>{label}</span>
        <strong>{value}</strong>
      </div>
  )
}

function ResponseItem({
                        icon,
                        text,
                      }: {
  icon: React.ReactNode
  text: string
}) {
  return (
      <div className="response-item">
        {icon}
        <span>{text}</span>
      </div>
  )
}

function ExplanationColumn({
                             title,
                             icon,
                             items,
                             positive = false,
                           }: {
  title: string
  icon: React.ReactNode
  items: LocalExplanation[]
  positive?: boolean
}) {
  const maxImpact = Math.max(
      ...items.map((item) =>
          Math.abs(item.shap_value),
      ),
      0.0001,
  )

  return (
      <div className="explanation-column">
        <div
            className={`explanation-title ${
                positive ? 'positive' : 'negative'
            }`}
        >
          {icon}
          {title}

          <span className="explanation-count">
          {items.length}
        </span>
        </div>

        {items.length === 0 ? (
            <div className="no-drivers">
              No significant drivers in this group.
            </div>
        ) : (
            <div className="explanation-items">
              {items.map((item) => {
                const magnitude =
                    (Math.abs(item.shap_value) /
                        maxImpact) *
                    100

                return (
                    <div
                        className="explanation-item"
                        key={item.feature}
                    >
                      <div className="explanation-item-top">
                        <div className="explanation-item-main">
                    <span>
                      {formatFeatureName(
                          item.feature,
                      )}
                    </span>

                          {item.shap_value > 0 ? (
                              <TrendingUp size={14} />
                          ) : (
                              <TrendingDown size={14} />
                          )}
                        </div>

                        <div className="explanation-value">
                          {item.shap_value > 0
                              ? '+'
                              : ''}
                          {item.shap_value.toFixed(4)}
                        </div>
                      </div>

                      <div className="impact-track">
                  <span
                      className="impact-fill"
                      style={{
                        width: `${magnitude}%`,
                      }}
                  />
                      </div>
                    </div>
                )
              })}
            </div>
        )}
      </div>
  )
}

export default App