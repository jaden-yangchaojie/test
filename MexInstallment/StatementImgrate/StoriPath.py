# sys
ChangeTime = "/api/admin/system/faketime"
QueryTime = "/api/credit/currentSystemTime"

# user
UserRegister = "/api/dflRegister"
UserLogin = "/api/dflLogin/"
UserGetContract = "/api/contract"
UserSignContract = "/v1.0/credit/contracts"
UserAddContract = "/api/addContract"
UserActivateCard = "/v1.0/credit/cards/activation"
UserReplaceCard = "/v1.0/credit/cards/replacement"

# trading
AppTradingAuth = '/v1.0/credit/authorizations'
AppTradingPayment = '/v1.0/credit/payments'
AppTradingPosting = '/v1.0/credit/authorizations/posting'
PomeloTradingAuth = '/transactions/authorizations'
PomeloTradingNotify = '/transactions/v1/notifications'
PomeloTradingPosting = '/backoffice/dfl-ng/credit/authorizations/posting'
PomeloTradingDebit = '/transactions/adjustments/debit'
PomeloTradingCredit = '/transactions/adjustments/credit'
    # adj
AdjTrading = '/backoffice/dfl-ng/credit/adjustment'

# statement
StatementCreate = "/backoffice/dfl/credit/statement/create"
StatementUnsettled = "/backoffice/dfl/credit/statement/unsettled"

# DQ
DQCreate = "/backoffice/dfl/credit/dqTask/create"
DQUpdate = "/backoffice/dfl/credit/dqDateUpdateTask/create"

# xxl-job
XXLJob = "/xxl-job-admin/jobinfo/trigger"

# mk
MKAddCrowdUser = "/v1.0/backoffice-ng/credit/marketing/crowds/users"
MKCancelBenefit = "/v1.0/backoffice-ng/credit/marketing/benefits/revisal/benefit"